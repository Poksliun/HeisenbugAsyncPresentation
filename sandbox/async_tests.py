# Файл для демонстрации работы асинхронного кода python

import asyncio
import time
from typing import Callable, Coroutine

from sandbox.plugs.async_api import AsyncDataBase, AsyncHttpClient

SLEEPING_SEC: int | float = 1
DOMAIN: str = 'heisenbug.com'
DB_CON: str = 'database.db'


async def first_test() -> bool:
    print('First test started')
    # Arrange
    client: AsyncHttpClient = AsyncHttpClient(url=DOMAIN, _delay=SLEEPING_SEC)
    db: AsyncDataBase = AsyncDataBase(connection=DB_CON, _delay=SLEEPING_SEC)
    await db.insert('inert into ...')
    # Act
    post_res: dict = await client.post('/post/req')
    get_res: dict = await client.get('/get/req')
    db_data: dict = await db.select('select * from ...')
    # Assert
    assert True
    print('First test finished')
    return True


async def second_test() -> bool:
    print('Second test started')
    await asyncio.sleep(SLEEPING_SEC)
    print('Second test finished')
    return True


async def third_test() -> bool:
    print('Third test started')
    await asyncio.sleep(SLEEPING_SEC)
    print('Third test finished')
    return True


async def main_with_locking():
    """Входная точка для запуска асинхронных тестов без использования задач
    """
    tests: list[Callable[[], Coroutine]] = [first_test, second_test, third_test]
    print('Start test run')
    start: float = time.time()
    results: list[bool] = [await test() for test in tests]
    end: float = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


async def main_without_locking():
    """Входная точка для запуска асинхронных тестов с использованием задач
    """
    tests: list[Callable[[], Coroutine]] = [first_test, second_test, third_test]
    tasks: list[asyncio.Task] = [asyncio.create_task(test()) for test in tests]
    print('Start test run')
    start: float = time.time()
    results: list[bool] = [await task for task in tasks]
    end: float = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


async def many_tests_without_locking_main():
    """Входная точка для запуска асинхронных тестов с использованием задач
    c возможностью корректирования количества запускаемых тестов
    """
    test_count: int = 20
    tests: list[Callable[[], Coroutine]] = [first_test for _ in range(test_count)]
    tasks: list[asyncio.Task] = [asyncio.create_task(test()) for test in tests]
    print('Start test run')
    start: float = time.time()
    results: list[bool] = [await task for task in tasks]
    end: float = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


if __name__ == '__main__':
    # asyncio.run(main_with_locking())
    # asyncio.run(main_without_locking())
    asyncio.run(many_tests_without_locking_main())
