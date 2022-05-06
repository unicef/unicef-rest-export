from django.contrib.auth import get_user_model

import factory

from demo.sample.models import Author, Book


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")

    class Meta:
        model = get_user_model()


class AuthorFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = Author


class BookFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    author = factory.SubFactory(AuthorFactory)
    description = factory.Faker("sentence", nb_words=200)

    class Meta:
        model = Book
