from rest_framework import serializers

from unicef_rest_export.serializers import ExportSerializer

from demo.sample.models import Author, Book


class BookListSerializer(ExportSerializer):
    class Meta:
        fields = (
            "id",
            "name",
        )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        list_serializer_class = BookListSerializer


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Author
        fields = "__all__"


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("first_name",)


class AuthorInvalidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
        list_serializer_class = AuthorListSerializer
