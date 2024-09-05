import asyncio
import os
import sqlite3
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor

import aiohttp
import aiosqlite
import pytest


@pytest.fixture(scope='session')
def domain() -> str:
    """Возвращает домен на который будут отсылаться запросы
    """
    return 'http://127.0.0.1:8000'


@pytest.fixture
def sync_db() -> sqlite3.Connection:
    """Возвращает синхронное подключение к базе данных.
    Закрывает подключение после выполнения теста в котором была вызвана
    """
    dir_name = os.path.dirname(__file__)
    connection = sqlite3.connect(f'{dir_name}/users_data.db')
    yield connection
    connection.close()


@pytest.fixture
async def async_db() -> aiosqlite.Connection:
    """Возвращает асинхронное подключение к базе данных.
    Закрывает подключение после выполнения теста в котором была вызвана
    """
    dir_name = os.path.dirname(__file__)
    connection = await aiosqlite.connect(f'{dir_name}/users_data.db')

    yield connection

    await connection.close()


@pytest.fixture
def get_event_loop() -> asyncio.AbstractEventLoop:
    """Возвращает действующий цикл событий
    """
    return asyncio.get_running_loop()


@pytest.fixture(scope='session')
def get_process_pool_executor() -> ProcessPoolExecutor:
    """Возвращает экземпляр ProcessPoolExecutor
    """
    with ProcessPoolExecutor() as p:
        yield p


@pytest.fixture(scope='session')
def get_thread_pool_executor() -> ThreadPoolExecutor:
    """Возвращает экземпляр ThreadPoolExecutor
    """
    with ThreadPoolExecutor() as p:
        yield p


@pytest.fixture(scope='session')
async def session() -> aiohttp.ClientSession:
    """Создает aiohttp.ClientSession для всех тестов.
    Закрывает aiohttp.ClientSession после завершения всех тестов
    """
    session_ = aiohttp.ClientSession()
    try:
        yield session_
    finally:
        await session_.close()
