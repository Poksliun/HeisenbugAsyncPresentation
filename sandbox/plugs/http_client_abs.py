from abc import ABC, abstractmethod
from typing import Optional


class ABCHttpClient(ABC):

    @abstractmethod
    def __init__(self, url: Optional[str] = None, _delay: int = 1) -> None:
        self.url = url
        self._delay = _delay

    @abstractmethod
    def get(self, path: str) -> Optional[dict]: ...

    @abstractmethod
    def post(self, path: str, body: Optional[dict] = None) -> Optional[dict]: ...
