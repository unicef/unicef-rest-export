from rest_framework.test import APIClient

import pytest

from tests import factories


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return factories.UserFactory()


@pytest.fixture
def superuser():
    return factories.UserFactory(
        username="superusername",
        email="super@example.com",
        is_superuser=True,
    )


@pytest.fixture
def author():
    return factories.AuthorFactory()


@pytest.fixture
def book():
    return factories.BookFactory()


@pytest.fixture
def books():
    class BookFactory:
        def get(self):
            return factories.BookFactory()

    return BookFactory()
