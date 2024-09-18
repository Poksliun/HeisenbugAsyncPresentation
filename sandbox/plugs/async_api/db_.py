import asyncio
from typing import Optional, Union

from sandbox.plugs.data_base_abs import ABCDataBase


class AsyncDataBase(ABCDataBase):

    def __init__(self, connection: Optional[str] = None, _delay: int = 1) -> None:
        self.connection: Optional[str] = connection
        self._delay: int = _delay

    async def select(self, query: Optional[str] = None) -> Optional[Union[dict, bool]]:
        print('select data from database')
        await asyncio.sleep(self._delay)
        return True

    async def insert(self, query: Optional[str] = None) -> None:
        print('insert data from database')
        await asyncio.sleep(self._delay)
