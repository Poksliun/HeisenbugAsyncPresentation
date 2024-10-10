import asyncio
from typing import Optional

import aiohttp
from pydantic import BaseModel


class UserProperty(BaseModel):
    name: str
    age: int
    property_type: str


class HttpClient:
    """Http клиент для отправки запросов на сервер
    """

    def __init__(self, domain: str, _delay: int = 0):
        self._domain: str = domain
        self._delay: int = _delay

    async def user_write(self, session: aiohttp.ClientSession, data: UserProperty) -> Optional[int]:
        url: str = self._domain + '/write'
        async with session.post(
                url=url,
                json=data.dict()
        ) as response:
            resp_body: Optional[dict] = await response.json()
            await asyncio.sleep(self._delay)
            return resp_body.get('id')
