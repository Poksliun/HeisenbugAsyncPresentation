import time
from typing import Optional, Union

from sandbox.plugs.data_base_abs import ABCDataBase


class DataBase(ABCDataBase):

    def __init__(self, connection: Optional[str] = None, _delay: int = 1) -> None:
        self.connection: Optional[str] = connection
        self._delay: int = _delay

    def select(self, query: Optional[str] = None) -> Optional[Union[dict, bool]]:
        print('select data from database')
        time.sleep(self._delay)
        return True

    def insert(self, query: Optional[str] = None) -> None:
        print('insert data from database')
        time.sleep(self._delay)
