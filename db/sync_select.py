import sqlite3
import time
from typing import Optional

__all__ = ['sync_get_user', 'sync_get_user_property']

SLEEP_TIME = .5


def sync_get_user(
        conn_obj: sqlite3.Cursor | sqlite3.Connection,
        id_: int | str
) -> Optional[sqlite3.Row]:
    """Выбрать одну запись из таблицы users с id равным id_

    Args:
        conn_obj: Объект, у которого есть метод execute, способный обращаться к базе данных
        id_: Число или строка идентификатор пользователя в базе данных
    """
    db_data: sqlite3.Cursor = conn_obj.execute(
        f'select * from users where id=:id',
        {'id': id_}
    )
    result = db_data.fetchone()
    time.sleep(SLEEP_TIME)
    return result


def sync_get_user_property(
        conn_obj: sqlite3.Cursor | sqlite3.Connection,
        id_: int | str
) -> Optional[sqlite3.Row]:
    """Выбрать одну запись из таблицы property с id равным id_

    Args:
        conn_obj: Объект, у которого есть метод execute, способный обращаться к базе данных
        id_: Число или строка идентификатор пользователя в базе данных
    """
    db_data = conn_obj.execute(
        f'select * from property where user_id=:id order by user_id',
        {'id': id_}
    )
    result: Optional[sqlite3.Row] = db_data.fetchone()
    time.sleep(SLEEP_TIME)
    return result
