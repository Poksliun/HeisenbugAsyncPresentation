"""SQLite была выбрана для демонстрации асинхронного api
только из-за нативной поддержки
как python и любыми операционными системами.
В sqlite отсутствует api создания пулов подключений и
обращения к ней происходят достаточно быстро, из-за чего
на практике результаты обращения к БД могут быть хуже.
Так же не стоит забывать, что база данных "Развернута"
локально, а все задержки при обращении к ней "эмулируются"
с помощью блокирующего time.sleep и неблокирующего asyncio.sleep.
"""

import sqlite3


def create_users_table(con: sqlite3.Connection):
    """Создает таблицу users
        Args:
            con: SQLite database connection object.
    """
    con.execute(
        """CREATE TABLE `users` (
                id INTEGER NOT NULL,
                name TEXT,
                age INTEGER,
                PRIMARY KEY (id)
                );"""
    )
    con.commit()


def create_property_table(con: sqlite3.Connection):
    """Создает таблицу property
        Args:
            con: SQLite database connection object.
    """
    con.execute(
        """CREATE TABLE `property` (
                user_id int,
                property_type text,
                FOREIGN KEY (user_id) REFERENCES `users`(id)
                );"""
    )
    con.commit()


def check_table(con: sqlite3.Connection) -> bool:
    """Проверяет наличие двух таблиц users и property в БД users_data.db
        Args:
            con: SQLite database connection object.
    """
    res = con.execute(
        """SELECT count(name)
            FROM sqlite_master
            WHERE name in ('users', 'property');"""
    ).fetchone()[0]
    if res == 2:
        return True
    return False


if __name__ == '__main__':
    with sqlite3.connect("users_data.db") as connection:
        if check_table(connection):
            pass
        else:
            try:
                create_users_table(connection)
            except Exception as exc:
                print(exc)
            try:
                create_property_table(connection)
            except Exception as exc:
                print(exc)
