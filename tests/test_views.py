import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_view(api_client, author):
    url = reverse("sample:author-normal")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    data = response.json()[0]
    assert data["id"] == author.pk
    assert data["first_name"] == author.first_name
    assert data["last_name"] == author.last_name
    assert len(data["books"]) == 0


def test_export_view_default_empty(api_client):
    response = api_client.get(reverse("sample:author-view"))
    assert response.status_code == 200
    assert b"<tr></tr>" in response.content


def test_export_view_default(api_client, author):
    response = api_client.get(reverse("sample:author-view"))
    assert response.status_code == 200
    assert str.encode(author.first_name) in response.content


def test_export_view_json_empty(api_client):
    url = "{}?format=json".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == [[]]


def test_export_view_json(api_client, author):
    url = "{}?format=json".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    data = response.json()[0]
    assert data["id"] == author.pk
    assert data["first_name"] == author.first_name
    assert data["last_name"] == author.last_name
    assert len(data["books"]) == 0


def test_export_view_xls_empty(api_client):
    url = "{}?format=xls".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_xls(api_client, author):
    url = "{}?format=xls".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_csv_empty(api_client):
    url = "{}?format=csv".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_csv(api_client, author):
    url = "{}?format=csv".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_invalid_format(api_client, author):
    url = "{}?format=wrong".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 404


def test_export_viewset(api_client, author):
    response = api_client.get(reverse("sample:author-list"))
    assert response.status_code == 200
    assert str.encode(author.first_name) in response.content


def test_export_view_meta_json(api_client, book):
    url = "{}?format=json".format(reverse("sample:book-view"))
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    data = response.json()[0]
    assert data["id"] == book.pk
    assert data["name"] == book.name
    assert data["author"] == book.author.pk


def test_export_view_many_json(api_client, book):
    url = "{}?format=json".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    data = response.json()[0]
    assert data["id"] == book.author.pk
    assert data["first_name"] == book.author.first_name
    assert data["last_name"] == book.author.last_name
    assert len(data["books"]) == 1
    data_book = data["books"][0]
    assert data_book["id"] == book.pk
    assert data_book["name"] == book.name
    assert data_book["author"] == book.author.pk


def test_export_view_invalid(api_client, author):
    """If list serializer extends ListSerializer instead of ExportSerializer"""
    url = "{}?format=json".format(reverse("sample:author-invalid"))
    with pytest.raises(Exception):
        api_client.get(url)


def test_export_view_get_template_context(api_client, author):
    response = api_client.get(reverse("sample:author-template"))
    assert response.status_code == 200
    assert str.encode(author.first_name) in response.content
    assert b"Sample Home" in response.content