import asyncio
from typing import Optional

import aiosqlite

__all__ = [
    'async_get_user',
    'async_get_user_property',
    'async_get_user_task',
    'async_get_user_property_task'
]

SLEEP_TIME = .5


async def async_get_user(
        conn_obj: aiosqlite.Cursor | aiosqlite.Connection,
        id_: int | str
) -> Optional[aiosqlite.Row]:
    """Сопрограмма выбора одой записи из таблицы users с id равным id_

    Args:
        conn_obj: Объект, у которого есть метод execute, способный обращаться к базе данных
        id_: Число или строка идентификатор пользователя в базе данных
    """
    db_data: aiosqlite.Cursor = await conn_obj.execute(
        f'select * from users where id=:id',
        {'id': id_}
    )
    result: Optional[aiosqlite.Row] = await db_data.fetchone()
    await asyncio.sleep(SLEEP_TIME)
    return result


async def async_get_user_property(
        conn_obj: aiosqlite.Cursor | aiosqlite.Connection,
        id_: int | str
) -> Optional[aiosqlite.Row]:
    """Сопрограмма выбора одой записи из таблицы property с user_id равным id_

    Args:
        conn_obj: Объект, у которого есть метод execute, способный обращаться к базе данных
        id_: Число или строка идентификатор пользователя в базе данных
    """
    db_data: aiosqlite.Cursor = await conn_obj.execute(
        f'select * from property where user_id=:id order by user_id',
        {'id': id_}
    )
    result: Optional[aiosqlite.Row] = await db_data.fetchone()
    await asyncio.sleep(SLEEP_TIME)
    return result


def async_get_user_task(
        conn_obj: aiosqlite.Cursor | aiosqlite.Connection,
        id_: int | str
) -> asyncio.Task[aiosqlite.Row]:
    """Функция "декоратор" возвращающая задачу поверх сопрограммы async_get_user
    """
    return asyncio.create_task(async_get_user(conn_obj, id_))


def async_get_user_property_task(
        conn_obj: aiosqlite.Cursor | aiosqlite.Connection,
        id_: int | str
) -> asyncio.Task[aiosqlite.Row]:
    """Функция "декоратор" возвращающая задачу поверх сопрограммы async_get_user_property
    """
    return asyncio.create_task(async_get_user_property(conn_obj, id_))
