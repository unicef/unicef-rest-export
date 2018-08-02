import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from tablib import Dataset
from tests.factories import BookFactory, UserFactory


@pytest.mark.django_db
def test_friendly_renderer():
    user = UserFactory(is_superuser=True)
    BookFactory()
    BookFactory(best_seller=True)

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(reverse('sample:book-list') + '?format=csv')

    dataset = Dataset().load(response.content.decode('utf-8'), 'csv')
    assert len(dataset._get_headers()) == 8
    assert dataset[0] == ('1', '1', 'David Hale', 'YJYmXlYXbEQVHdGkjhPS', 'Nancy', '1', 'Spencer', '')
    assert dataset[1] == ('', '', '2', 'Random', '', '')
