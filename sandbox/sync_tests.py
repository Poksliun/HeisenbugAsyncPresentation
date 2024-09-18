# Файл для демонстрации работы обычного синхронного кода python

import time
from typing import Callable

from sandbox.plugs.sync_api import DataBase, HttpClient

SLEEPING_SEC: int | float = 1
DOMAIN: str = 'heisenbug.com'
DB_CON: str = 'database.db'


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


def main():
    """Входная точка для запуска тестов в один поток, один процесс
    """
    tasks: list[Callable[[], bool]] = [first_test, second_test, third_test]
    print('Start test run')
    start: float = time.time()
    results: list[bool] = [task() for task in tasks]
    end: float = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


def many_test_main():
    """Входная точка для запуска тестов в один поток, один процесс
    с возможностью корректирования количества запускаемых тестов
    """
    test_count: int = 20
    tests: list[Callable[[], bool]] = [first_test for _ in range(test_count)]
    print('Start test run')
    start: float = time.time()
    results: list[bool] = [test() for test in tests]
    end: float = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


if __name__ == '__main__':
    main()  # ~ 6 sec
    # many_test_main()  # ~ 80 sec
