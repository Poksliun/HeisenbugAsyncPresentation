import asyncio
import logging

import databases
from fastapi import FastAPI, status, Response
from pydantic import BaseModel

logging.basicConfig(format='%(asctime)s - %(message)')
logger = logging.getLogger(__name__)

DB_HOST = 'users_data.db'
SLEEP_TIME = .5

database = databases.Database(f'sqlite+aiosqlite:///{DB_HOST}')

app = FastAPI()


@app.on_event("startup")
async def startup():
    # когда приложение запускается устанавливаем соединение с БД
    await database.connect()
    # Настройка WAL позволяет читать из БД не дожидаясь записи и наоборот
    await database.execute("PRAGMA journal_mode=WAL")


@app.on_event("shutdown")
async def shutdown():
    # когда приложение останавливается разрываем соединение с БД
    await database.disconnect()


class User(BaseModel):
    id: int | None = None
    name: str
    age: int


class Property(BaseModel):
    user_id: int
    property_type: str


class UserProperty(BaseModel):
    name: str
    age: int
    property_type: str


@app.post('/write', status_code=status.HTTP_201_CREATED)
async def write_to_db(up: UserProperty, response: Response):
    await asyncio.sleep(SLEEP_TIME)
    try:
        async with database.connection() as conn:
            async with conn.transaction():
                user_id = await conn.execute(f'insert into users (name, age) '
                                             f'values (:name, :age) returning id',
                                             {'name': up.name, 'age': up.age})
                if property_type := up.property_type:
                    property_ = Property(user_id=user_id, property_type=property_type)
                    await conn.execute(
                        f'insert into property (user_id, property_type) '
                        f'values (:uid, :p_type)',
                        {'uid': property_.user_id, 'p_type': property_.property_type})
            return {'id': user_id}
    except Exception as exc:
        logger.exception(exc)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None


@app.get('/read/{name}', status_code=status.HTTP_200_OK)
async def read_from_db(name, response: Response):
    await asyncio.sleep(SLEEP_TIME)
    name = str(name)
    try:
        async with database.connection() as conn:
            user_db = await conn.fetch_all(
                f'select * from users where name = :name',
                {'name': name}
            )
            print(user_db)
        data = [
            User(id=i_data[0], name=i_data[1], age=i_data[2]).model_dump()
            for i_data in user_db
        ]
        return data
    except Exception as exc:
        logger.exception(exc)
        response.status_code = status.HTTP_400_BAD_REQUEST
