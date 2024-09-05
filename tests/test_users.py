import asyncio
import random
import time
import sqlite3
import functools
from typing import Awaitable

import pytest
import requests
import aiohttp
import aiosqlite

from db.async_select import (
    async_get_user,
    async_get_user_property
)

from db.sync_select import (
    sync_get_user,
    sync_get_user_property
)

MANY_TEST_COUNT = 100
FEW_TEST_COUNT = 8


def create_random_number() -> int:
    return random.randint(0, 99999)


def cpu_bound_func(sec: int = 5):
    # todo: Переделать под настоящую счетную функцию
    print('Start cpu bound func')
    time.sleep(sec)
    return sec


def lock_io_func(sec: int = 5):
    print('Start lock io func')
    time.sleep(sec)
    return sec


class TestUsers:
    WRITE_END_POINT = '/write'
    READ_END_POINT = '/read'
    MIN_AGE = 20
    MAX_AGE = 40
    PROPERTY_TYPE = 'flat'

    @pytest.mark.parametrize('iterator', list(range(MANY_TEST_COUNT)))
    def test_users_write(
            self,
            check,
            domain,
            iterator,
            sync_db
    ):
        # Arrange
        name = f'test_{create_random_number():0>4}'
        age = random.randint(self.MIN_AGE, self.MAX_AGE)
        # Act
        resp = requests.post(
            url=domain + self.WRITE_END_POINT,
            json={
                'name': name,
                'age': age,
                'property_type': self.PROPERTY_TYPE
            }
        )
        id_: int = resp.json().get('id')
        # Assert
        user: sqlite3.Row = sync_get_user(sync_db, id_)
        with check:
            assert user[1] == name
            assert user[2] == age
        user_property: sqlite3.Row = sync_get_user_property(sync_db, id_)
        with check:
            assert user_property[1] == self.PROPERTY_TYPE

    @pytest.mark.parametrize('iterator', list(range(0, MANY_TEST_COUNT)))
    @pytest.mark.asyncio_cooperative
    async def test_async_users_write(
            self,
            check,
            domain,
            iterator,
            async_db,
    ):
        # Arrange
        name: str = f'test_{create_random_number():0>4}'
        age: int = random.randint(self.MIN_AGE, self.MAX_AGE)
        # Act
        async with aiohttp.ClientSession() as cs:
            async with cs.post(
                    url=domain + self.WRITE_END_POINT,
                    json={
                        'name': name,
                        'age': age,
                        'property_type': self.PROPERTY_TYPE
                    }
            ) as resp:
                body: dict = await resp.json()
                id_: int = body.get('id')
        # Assert
        user: aiosqlite.Row = await async_get_user(async_db, id_)
        with check:
            assert user[1] == name
            assert user[2] == age
        user_property: aiosqlite.Row = await async_get_user_property(async_db, id_)
        with check:
            assert user_property[1] == self.PROPERTY_TYPE

    @pytest.mark.parametrize('iterator', list(range(0, MANY_TEST_COUNT)))
    @pytest.mark.asyncio_cooperative
    async def test_async_users_write_optimize(
            self,
            check,
            domain,
            iterator,
            async_db,
    ):
        # Arrange
        name: str = f'test_{create_random_number():0>4}'
        age: int = random.randint(self.MIN_AGE, self.MAX_AGE)
        # Act
        async with aiohttp.ClientSession() as cs:
            async with cs.post(
                    url=domain + self.WRITE_END_POINT,
                    json={
                        'name': name,
                        'age': age,
                        'property_type': self.PROPERTY_TYPE
                    }
            ) as resp:
                body: dict = await resp.json()
                id_: int = body.get('id')
        # Assert
        user: asyncio.Task = asyncio.create_task(async_get_user(async_db, id_))
        user_property: asyncio.Task = asyncio.create_task(
            async_get_user_property(async_db, id_))
        with check:
            user: aiosqlite.Row = await user
            assert user[1] == name
            assert user[2] == age
        with check:
            user_property: aiosqlite.Row = await user_property
            assert user_property[1] == self.PROPERTY_TYPE

    @pytest.mark.parametrize('iterator', list(range(0, FEW_TEST_COUNT)))
    @pytest.mark.asyncio_cooperative
    async def test_async_users_write_with_cpu_bound_task(
            self,
            check,
            domain,
            iterator,
            async_db,
            get_event_loop,
            get_process_pool_executor
    ):
        # Arrange
        name: str = f'test_{create_random_number():0>4}'
        age: int = random.randint(self.MIN_AGE, self.MAX_AGE)
        # Act
        async with aiohttp.ClientSession() as cs:
            async with cs.post(
                    url=domain + self.WRITE_END_POINT,
                    json={
                        'name': name,
                        'age': age,
                        'property_type': self.PROPERTY_TYPE
                    }
            ) as resp:
                body: dict = await resp.json()
                id_: int = body.get('id')
        cpu_bound_res = get_event_loop.run_in_executor(get_process_pool_executor,
                                                       functools.partial(cpu_bound_func, 5))
        # Assert
        user: Awaitable[aiosqlite.Row] = asyncio.create_task(async_get_user(async_db, id_))
        user_property: Awaitable[aiosqlite.Row] = asyncio.create_task(
            async_get_user_property(async_db, id_))
        with check:
            user: aiosqlite.Row = await user
            assert user[1] == name
            assert user[2] == age
        with check:
            user_property: aiosqlite.Row = await user_property
            assert user_property[1] == self.PROPERTY_TYPE
        with check:
            assert await cpu_bound_res == 5

    @pytest.mark.parametrize('iterator', list(range(0, FEW_TEST_COUNT)))
    @pytest.mark.asyncio_cooperative
    async def test_async_users_write_with_lock_io_task(
            self,
            check,
            domain,
            iterator,
            async_db,
            get_event_loop,
            get_thread_pool_executor
    ):
        # Arrange
        name: str = f'test_{create_random_number():0>4}'
        age: int = random.randint(self.MIN_AGE, self.MAX_AGE)
        # Act
        async with aiohttp.ClientSession() as cs:
            async with cs.post(
                    url=domain + self.WRITE_END_POINT,
                    json={
                        'name': name,
                        'age': age,
                        'property_type': self.PROPERTY_TYPE
                    }
            ) as resp:
                body: dict = await resp.json()
                id_: int = body.get('id')
        lock_io_res = get_event_loop.run_in_executor(get_thread_pool_executor,
                                                     functools.partial(lock_io_func, 5))
        # Assert
        user: asyncio.Task = asyncio.create_task(async_get_user(async_db, id_))
        user_property: asyncio.Task = asyncio.create_task(
            async_get_user_property(async_db, id_))
        with check:
            user: aiosqlite.Row = await user
            assert user[1] == name
            assert user[2] == age
        with check:
            user_property: aiosqlite.Row = await user_property
            assert user_property[1] == self.PROPERTY_TYPE
        with check:
            assert await lock_io_res == 5
