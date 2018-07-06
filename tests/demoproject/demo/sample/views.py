from demo.sample import serializers
from demo.sample.models import Author, Book
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer

from unicef_rest_export.views import ExportMixin, ExportView, ExportViewSet


class AuthorNormalView(ExportMixin, ListAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    renderer_classes = (JSONRenderer, )


class AuthorView(ExportView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer


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


class BookView(ExportView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
