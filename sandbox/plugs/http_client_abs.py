from abc import ABC, abstractmethod
from typing import Optional, Union


class ABCHttpClient(ABC):

    @abstractmethod
    def __init__(self, url: Optional[str] = None, _delay: int = 1) -> None:
        self.url: str = url
        self._delay: int = _delay

    @abstractmethod
    def get(self, path: str) -> Optional[Union[dict, bool]]: ...

    @abstractmethod
    def post(self, path: str, body: Optional[dict] = None) -> Optional[Union[dict, bool]]: ...
