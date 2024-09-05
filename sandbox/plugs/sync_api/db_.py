import time
from typing import Optional

from sandbox.plugs.data_base_abs import ABCDataBase


class DataBase(ABCDataBase):

    def __init__(self, connection: Optional[str] = None, _delay: int = 1) -> None:
        self.connection = connection
        self._delay = _delay

    def select(self, query: Optional[str] = None) -> Optional[dict]:
        print('select data from database')
        time.sleep(self._delay)
        return

    def insert(self, query: Optional[str] = None) -> None:
        print('insert data from database')
        time.sleep(self._delay)
