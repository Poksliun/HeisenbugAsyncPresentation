from abc import ABC, abstractmethod
from typing import Optional


class ABCDataBase(ABC):

    @abstractmethod
    def __init__(self, connection: Optional[str] = None, _delay: int = 1) -> None:
        self.connection = connection
        self._delay = _delay

    @abstractmethod
    def select(self, query: Optional[str] = None) -> Optional[dict]: ...

    @abstractmethod
    def insert(self, query: Optional[str] = None) -> None: ...
