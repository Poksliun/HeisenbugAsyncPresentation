# Файл для демонстрации работы обычного синхронного кода python

import time

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
    """Входная точка для запуска тестов в один поток, один процесс
    """
    tasks = [first_test, second_test, third_test]
    print('Start test run')
    start = time.time()
    results = [task() for task in tasks]
    end = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


def many_test_main():
    """Входная точка для запуска тестов в один поток, один процесс
    с возможностью корректирования количества запускаемых тестов
    """
    test_count = 20
    tests = [first_test for _ in range(test_count)]
    print('Start test run')
    start = time.time()
    results = [test() for test in tests]
    end = time.time()
    if all(results):
        print('All tests Successfully')
    else:
        print('All test not Successfully')
    print(f'Tests runs in {end - start} sec.')


if __name__ == '__main__':
    main()
    # many_test_main()
