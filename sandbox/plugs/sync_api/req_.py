# req_.py

import time
from typing import Optional

from sandbox.plugs.http_client_abs import ABCHttpClient


class HttpClient(ABCHttpClient):

    def __init__(self, url: Optional[str] = None, _delay: int = 1) -> None:
        self.url = url
        self._delay = _delay

    def get(self, path: str) -> Optional[dict]:
        print(f'\tSend sync get req to {self.url + path}')
        time.sleep(self._delay)
        return

    def post(self, path: str, body: Optional[dict] = None) -> Optional[dict]:
        print(f'\tSend sync post req to {self.url + path}, with body {body}')
        time.sleep(self._delay)
        return
