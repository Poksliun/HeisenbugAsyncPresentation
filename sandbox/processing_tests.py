# Демонстрация работы многопроцессорного кода python

import time
import multiprocessing
from multiprocessing.pool import Pool
from typing import Callable

from sandbox.plugs.sync_api import DataBase, HttpClient

SLEEPING_SEC: int | float = 1
DOMAIN: str = 'heisenbug.com'
DB_CON: str = 'database.db'
PROCESS_COUNT: int = multiprocessing.cpu_count()


def first_test() -> bool:
    print('First test started')
    # Arrange
    client: HttpClient = HttpClient(url=DOMAIN, _delay=SLEEPING_SEC)
    db: DataBase = DataBase(connection=DB_CON, _delay=SLEEPING_SEC)
    db.insert('inert into ...')
    # Act
    post_res: dict = client.post('/post/req')
    get_res: dict = client.get('/get/req')
    db_data: dict = db.select('select * from ...')
    # Assert
    assert post_res
    assert get_res
    assert db_data
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


def main() -> None:
    """Входная точка для запуска тестов на нескольких ядрах процессора
    """
    tests: list[Callable[[], bool]] = [first_test, second_test, third_test]
    with Pool(processes=3) as p:
        print('Start test run')
        start: float = time.time()
        runner: list[multiprocessing.pool.ApplyResult] = [p.apply_async(test) for test in tests]
        results: list[bool] = [task.get() for task in runner]
        end: float = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


def many_test_main():
    """Входная точка для запуска тестов на нескольких ядрах процессора
    с возможностью корректирования количества запускаемых тестов
    """
    test_count: int = 20
    tests: list[Callable[[], bool]] = [first_test for _ in range(test_count)]
    with Pool(PROCESS_COUNT) as p:
        print('Start test run')
        start: float = time.time()
        runner: list[multiprocessing.pool.ApplyResult] = [p.apply_async(test) for test in tests]
        results: list[bool] = [task.get() for task in runner]
        end: float = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


if __name__ == '__main__':
    # main()  # ~ 4 sec
    many_test_main()  # ~ 12 sec
