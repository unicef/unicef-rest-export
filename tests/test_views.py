import factory
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from tablib import Dataset
from tests.factories import BookFactory, UserFactory

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


def test_export_view_list(api_client, author):
    response = api_client.get(reverse("sample:author-view"))
    assert response.status_code == 200
    assert str.encode(author.first_name) in response.content


def test_export_view_list_json_empty(api_client):
    url = "{}?format=json".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == [[]]


def test_export_view_list_json(api_client, author):
    url = "{}?format=json".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    data = response.json()[0]
    assert data["ID"] == author.pk
    assert data["First name"] == author.first_name
    assert data["Last name"] == author.last_name
    assert len(data["Books"]) == 0


def test_export_view_list_xls_empty(api_client):
    url = "{}?format=xls".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_xls(api_client, author):
    url = "{}?format=xls".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_view_retrieve(api_client, book):
    response = api_client.get(reverse("sample:book-detail", args=[book.pk]))
    assert response.status_code == 200


def test_export_view_retrieve_xls(api_client, book):
    url = "{}?format=xls".format(
        reverse("sample:book-detail", args=[book.pk])
    )
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_xlsx_empty(api_client):
    url = "{}?format=xlsx".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_xlsx(api_client, author):
    url = "{}?format=xlsx".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_retrieve_xlsx(api_client, book):
    url = "{}?format=xlsx".format(
        reverse("sample:book-detail", args=[book.pk])
    )
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_csv_empty(api_client):
    url = "{}?format=csv".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_csv(api_client, author):
    url = "{}?format=csv".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_retrieve_csv(api_client, book):
    url = "{}?format=csv".format(
        reverse("sample:book-detail", args=[book.pk])
    )
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_pdf_empty(api_client):
    url = "{}?format=pdf".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_pdf_table_empty(api_client):
    url = "{}?format=pdf_table".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_docx_empty(api_client):
    url = "{}?format=docx".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_pdf(api_client, author):
    url = "{}?format=pdf".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_retrieve_pdf(api_client, book):
    url = "{}?format=pdf".format(
        reverse("sample:book-detail", args=[book.pk])
    )
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_pdf_table(api_client, author):
    url = "{}?format=pdf_table".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_retrieve_pdf_table(api_client, book):
    url = "{}?format=pdf_table".format(
        reverse("sample:book-detail", args=[book.pk])
    )
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_docx(api_client, author):
    url = "{}?format=docx".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_retrieve_docx(api_client, book):
    url = "{}?format=docx".format(
        reverse("sample:book-detail", args=[book.pk])
    )
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_invalid_format(api_client, author):
    url = "{}?format=wrong".format(reverse("sample:author-view"))
    response = api_client.get(url)
    assert response.status_code == 404


def test_export_viewset_list(api_client, author):
    response = api_client.get(reverse("sample:author-list"))
    assert response.status_code == 200
    assert str.encode(author.first_name) in response.content


def test_export_view_foreignkey_list_json(api_client, book):
    url = "{}?format=json".format(reverse("sample:book-view"))
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    data = response.json()[0]
    assert data["ID"] == book.pk
    assert data["Name"] == book.name
    assert data["Author"] == book.author.pk


def test_export_view_foreignkey_list_xls(api_client, book):
    url = "{}?format=xls".format(reverse("sample:book-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_foreignkey_list_xlsx(api_client, book):
    url = "{}?format=xlsx".format(reverse("sample:book-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_foreignkey_list_csv(api_client, book):
    url = "{}?format=csv".format(reverse("sample:book-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_foreignkey_list_pdf(api_client, book):
    url = "{}?format=pdf".format(reverse("sample:book-view"))
    response = api_client.get(url)
    with open("/tmp/file.pdf", "wb") as fp:
        fp.write(response.content)
    assert response.status_code == 200


def test_export_view_foreignkey_list_pdf_table(api_client, book):
    url = "{}?format=pdf_table".format(reverse("sample:book-view"))
    response = api_client.get(url)
    with open("/tmp/file_table.pdf", "wb") as fp:
        fp.write(response.content)
    assert response.status_code == 200


def test_export_view_foreignkey_list_docx(api_client, book):
    url = "{}?format=docx".format(reverse("sample:book-view"))
    response = api_client.get(url)
    with open("/tmp/file.docx", "wb") as fp:
        fp.write(response.content)
    assert response.status_code == 200


def test_export_view_list_pdf_text_blob(api_client):
    BookFactory(description=factory.Faker("sentence", nb_words=800))
    url = "{}?format=pdf".format(reverse("sample:book-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_pdf_table_text_blob(api_client):
    BookFactory(description=factory.Faker("sentence", nb_words=800))
    url = "{}?format=pdf_table".format(reverse("sample:book-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_docx_text_blob(api_client):
    BookFactory(description=factory.Faker("sentence", nb_words=800))
    url = "{}?format=docx".format(reverse("sample:book-view"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_transform_json(api_client, book):
    url = "{}?format=json".format(reverse("sample:author-transform"))
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    data = response.json()[0]
    assert data["ID"] == book.author.pk
    assert data["First name"] == book.author.first_name
    assert data["Last name"] == book.author.last_name
    assert data["Books"] == [book.name]


def test_export_view_list_transform_xls(api_client, book):
    url = "{}?format=xls".format(reverse("sample:author-transform"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_transform_xlsx(api_client, book):
    url = "{}?format=xlsx".format(reverse("sample:author-transform"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_transform_csv(api_client, book):
    url = "{}?format=csv".format(reverse("sample:author-transform"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_transform_pdf(api_client, book):
    url = "{}?format=pdf".format(reverse("sample:author-transform"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_transform_pdf_table(api_client, book):
    url = "{}?format=pdf_table".format(reverse("sample:author-transform"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_transform_docx(api_client, book):
    url = "{}?format=docx".format(reverse("sample:author-transform"))
    response = api_client.get(url)
    assert response.status_code == 200


def test_export_view_list_invalid(api_client, author):
    """If list serializer extends ListSerializer instead of ExportSerializer"""
    url = "{}?format=json".format(reverse("sample:author-invalid"))
    with pytest.raises(Exception):
        api_client.get(url)


def test_export_view_list_get_template_context(api_client, author):
    response = api_client.get(reverse("sample:author-template"))
    assert response.status_code == 200
    assert str.encode(author.first_name) in response.content
    assert b"Sample Home" in response.content


@pytest.mark.django_db
def test_export_model_view():
    user = UserFactory(is_superuser=True)
    BookFactory(name='demo')
    BookFactory(name='test')

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('sample:author-list') + '?format=csv'
    response = client.get(url, format='json')

    dataset = Dataset().load(response.content.decode('utf-8'), 'csv')
    assert len(dataset._get_headers()) == 4
    assert dataset.headers == ['ID', 'Books', 'First name', 'Last name']
