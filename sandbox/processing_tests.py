# Демонстрация работы многопроцессорного кода python

import time
import multiprocessing
from multiprocessing.pool import Pool

from sandbox.plugs.sync_api import DataBase, HttpClient

SLEEPING_SEC = 1
DOMAIN = 'heisenbug.com'
DB_CON = 'database.db'


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
    print('Second test started')
    time.sleep(SLEEPING_SEC)
    print('Second test finished')
    return True


def third_test() -> bool:
    print('Third test started')
    time.sleep(SLEEPING_SEC)
    print('Third test finished')
    return True


def main():
    """Входная точка для запуска тестов на нескольких ядрах процессора
    """
    tasks = [first_test, second_test, third_test]
    with Pool() as p:
        print('Start test run')
        start = time.time()
        runner = [p.apply_async(task) for task in tasks]
        results = [task.get() for task in runner]
        end = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


def many_test_main():
    """Входная точка для запуска тестов на нескольких ядрах процессора
    с возможностью корректирования количества запускаемых тестов
    """
    test_count = 20
    tests = [first_test for _ in range(test_count)]
    with Pool(processes=multiprocessing.cpu_count()) as p:
        print('Start test run')
        start = time.time()
        runner = [p.apply_async(test) for test in tests]
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
