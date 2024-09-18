from abc import ABC, abstractmethod
from typing import Optional, Union


class ABCDataBase(ABC):

    @abstractmethod
    def __init__(self, connection: Optional[str] = None, _delay: int = 1) -> None:
        self.connection: Optional[str] = connection
        self._delay: int = _delay

    @abstractmethod
    def select(self, query: Optional[str] = None) -> Optional[Union[dict, bool]]: ...

    @abstractmethod
    def insert(self, query: Optional[str] = None) -> None: ...
