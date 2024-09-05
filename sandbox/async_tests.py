# Файл для демонстрации работы асинхронного кода python

import asyncio
import time

from sandbox.plugs.async_api import DataBase, HttpClient

SLEEPING_SEC = 1
DOMAIN = 'heisenbug.com'
DB_CON = 'database.db'


async def first_test() -> bool:
    print('First test started')
    # Arrange
    client = HttpClient(url=DOMAIN, _delay=SLEEPING_SEC)
    db = DataBase(connection=DB_CON, _delay=SLEEPING_SEC)
    await db.insert('inert into ...')
    # Act
    post_res = await client.post('/post/req')
    get_res = await client.get('/get/req')
    db_data = await db.select('select * from ...')
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
    tests = [first_test, second_test, third_test]
    print('Start test run')
    start = time.time()
    results = [await test() for test in tests]
    end = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


async def main_without_locking():
    """Входная точка для запуска асинхронных тестов с использованием задач
    """
    tests = [first_test, second_test, third_test]
    tasks = [asyncio.create_task(test()) for test in tests]
    print('Start test run')
    start = time.time()
    results = [await task for task in tasks]
    end = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


async def many_tests_without_locking_main():
    """Входная точка для запуска асинхронных тестов с использованием задач
    c возможностью корректирования количества запускаемых тестов
    """
    test_count = 20
    tests = [first_test for _ in range(test_count)]
    tasks = [asyncio.create_task(test()) for test in tests]
    print('Start test run')
    start = time.time()
    results = [await task for task in tasks]
    end = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


if __name__ == '__main__':
    asyncio.run(main_with_locking())
    # asyncio.run(main_without_locking())
    # asyncio.run(many_tests_without_locking_main())
