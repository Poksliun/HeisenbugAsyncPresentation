import random

import pytest

from db.async_select import (
    async_get_user_task,
    async_get_user_property_task
)

from src.http_client import (
    HttpClient,
    UserProperty
)

MANY_TEST_COUNT: int = 100


def create_random_number() -> int:
    return random.randint(0, 99999)


class TestUsers:
    WRITE_END_POINT: str = '/write'
    MIN_AGE: int = 20
    MAX_AGE: int = 40
    PROPERTY_TYPE: int = 'flat'

    @pytest.mark.parametrize('iterator', list(range(0, MANY_TEST_COUNT)))
    @pytest.mark.asyncio_cooperative
    async def test_async_pretty_write_user(
            self,
            check,
            domain,
            iterator,
            async_db,
            session
    ):
        # Arrange
        name = f'test_{create_random_number():0>4}'
        age = random.randint(self.MIN_AGE, self.MAX_AGE)
        data = UserProperty(name=name, age=age, property_type=self.PROPERTY_TYPE)
        client = HttpClient(domain)
        # Act
        user_id = await client.user_write(session, data=data)
        # Assert
        user = async_get_user_task(async_db, user_id)
        user_property = async_get_user_property_task(async_db, user_id)
        with check:
            user = await user
            assert user[1] == name
            assert user[2] == age
        with check:
            user_property = await user_property
            assert user_property[1] == self.PROPERTY_TYPE
