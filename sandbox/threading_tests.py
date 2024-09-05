# Демонстрация работы многопоточного кода python

import time
import multiprocessing
from multiprocessing.pool import ThreadPool

from sandbox.plugs.sync_api import DataBase, HttpClient

SLEEPING_SEC = 1
DOMAIN = 'heisenbug.com'
DB_CON = 'database.db'
THREAD_COUNT = multiprocessing.cpu_count() * 3


def first_test() -> bool:
    print('First test started')
    # Arrange
    client = HttpClient(url=DOMAIN, _delay=SLEEPING_SEC)
    db = DataBase(connection=DB_CON, _delay=SLEEPING_SEC)
    db.insert('inert into ...')
    # Act
    post_res = client.post('/post/req')
    get_res = client.get('/get/req')
    db_data = db.select('select * from ...')
    # Assert
    assert True
    print('First test finished')
    return True


def second_test() -> bool:
    print('\tSecond test started')
    time.sleep(SLEEPING_SEC)
    print('\tSecond test finished')
    return True


def third_test() -> bool:
    print('\tThird test started')
    time.sleep(SLEEPING_SEC)
    print('\tThird test finished')
    return True


def main():
    """Входная точка для запуска тестов на нескольких потоков
    внутри одного ядра процессора
    """
    tasks = [first_test, second_test, third_test]
    with ThreadPool() as tp:
        print('Start test run')
        start = time.time()
        runner = [tp.apply_async(task) for task in tasks]
        results = [task.get() for task in runner]
        end = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


def many_test_main():
    """Входная точка для запуска тестов на нескольких потоков
    внутри одного ядра процессора с возможностью корректирования количество
    запускаемых тестов
    """
    test_count = 20
    tests = [first_test for _ in range(test_count)]
    with ThreadPool(THREAD_COUNT) as tp:
        print('Start test run')
        start = time.time()
        runner = [tp.apply_async(test) for test in tests]
        results = [task.get() for task in runner]
        end = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


if __name__ == '__main__':
    main()
    # many_test_main()
