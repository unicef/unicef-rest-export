from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet

from unicef_rest_export.renderers import FriendlyCSVRenderer
from unicef_rest_export.views import ExportMixin, ExportModelView, ExportView, ExportViewBase, ExportViewSet

from demo.sample import serializers
from demo.sample.models import Author, Book


class AuthorNormalView(ExportMixin, ListAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    renderer_classes = (JSONRenderer,)


class AuthorView(ExportView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class AuthorTransformView(ExportView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer

    def transform_books(self, data):
        return [d["name"] for d in data]

    def transform_dataset(self, dataset):
        dataset.add_formatter("Books", self.transform_books)
        return dataset


class AuthorInvalidView(ExportView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorInvalidSerializer


class AuthorTemplateView(ExportView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer

    def get_template_context(self, data):
        data["home"] = "Sample Home"
        return data


class AuthorViewSet(ExportViewSet):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class BookViewSet(ExportViewBase, ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookView(ExportView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookCSVView(ExportModelView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer

    renderer_classes = (
        JSONRenderer,
        FriendlyCSVRenderer,
    )
