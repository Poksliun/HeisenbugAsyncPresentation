# req_.py

import time
from typing import Optional, Union

from sandbox.plugs.http_client_abs import ABCHttpClient


class HttpClient(ABCHttpClient):

    def __init__(self, url: Optional[str] = None, _delay: int = 1) -> None:
        self.url: Optional[str] = url
        self._delay: int = _delay

    def get(self, path: str) -> Optional[Union[dict, bool]]:
        print(f'\tSend sync get req to {self.url + path}')
        time.sleep(self._delay)
        return True

    def post(self, path: str, body: Optional[dict] = None) -> Optional[Union[dict, bool]]:
        print(f'\tSend sync post req to {self.url + path}, with body {body}')
        time.sleep(self._delay)
        return True
