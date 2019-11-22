from django.urls import reverse
from rest_framework.test import APIClient
from tablib import Dataset

import pytest

from tests.factories import BookFactory, UserFactory


@pytest.mark.xfail
@pytest.mark.django_db
def test_friendly_renderer():
    user = UserFactory(is_superuser=True)
    BookFactory()
    BookFactory(best_seller=True)

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(reverse('sample:book-csv-view') + '?format=csv')
    dataset = Dataset().load(response.content.decode('utf-8'), 'csv')
    assert len(dataset._get_headers()) == 4
    assert dataset[0][2] == ''
    assert dataset[1][2] == 'Yes'
