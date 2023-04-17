from django.urls import re_path
from rest_framework import routers

from demo.sample import views

app_name = "sample"

router = routers.DefaultRouter()
router.register(r"authors/", views.AuthorViewSet)
router.register(r"books/", views.BookViewSet)

urlpatterns = [
    re_path(r"^author/normal/$", views.AuthorNormalView.as_view(), name="author-normal"),
    re_path(r"^author/$", views.AuthorView.as_view(), name="author-view"),
    re_path(
        r"^author/transform/$",
        views.AuthorTransformView.as_view(),
        name="author-transform",
    ),
    re_path(r"^author/invalid/$", views.AuthorInvalidView.as_view(), name="author-invalid"),
    re_path(
        r"^author/template/$",
        views.AuthorTemplateView.as_view(),
        name="author-template",
    ),
    re_path(r"^book/$", views.BookView.as_view(), name="book-view"),
    re_path(r"^book/csv/$", views.BookCSVView.as_view(), name="book-csv-view"),
]

urlpatterns += router.urls
