# req_.py

import asyncio
from typing import Optional

from sandbox.plugs.http_client_abs import ABCHttpClient


class HttpClient(ABCHttpClient):

    def __init__(self, url: Optional[str] = None, _delay: int = 1) -> None:
        self.url = url
        self._delay = _delay

    async def get(self, path: str) -> Optional[dict]:
        print(f'\tSend async get req to {self.url + path}')
        await asyncio.sleep(self._delay)
        return

    async def post(self, path: str, body: Optional[dict] = None) -> Optional[dict]:
        print(f'\tSend async post req to {self.url + path}, with body {body}')
        await asyncio.sleep(self._delay)
        return
