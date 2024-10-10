# req_.py

import asyncio
from typing import Optional, Union

from sandbox.plugs.http_client_abs import ABCHttpClient


class AsyncHttpClient(ABCHttpClient):

    def __init__(self, url: Optional[str] = None, _delay: int = 1) -> None:
        self.url: Optional[str] = url
        self._delay: int = _delay

    async def get(self, path: str) -> Optional[Union[dict, bool]]:
        print(f'\tSend async get req to {self.url + path}')
        await asyncio.sleep(self._delay)
        return True

    async def post(self, path: str, body: Optional[dict] = None) -> Optional[Union[dict, bool]]:
        print(f'\tSend async post req to {self.url + path}, with body {body}')
        await asyncio.sleep(self._delay)
        return True
