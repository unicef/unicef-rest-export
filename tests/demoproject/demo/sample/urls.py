from django.conf.urls import url
from rest_framework import routers

from demo.sample import views

app_name = 'sample'

router = routers.DefaultRouter()
router.register(r'authors/', views.AuthorViewSet)
router.register(r'books/', views.BookViewSet)

urlpatterns = [
    url(
        r'^author/normal/$',
        views.AuthorNormalView.as_view(),
        name='author-normal'
    ),
    url(r'^author/$', views.AuthorView.as_view(), name='author-view'),
    url(
        r'^author/transform/$',
        views.AuthorTransformView.as_view(),
        name='author-transform'
    ),
    url(
        r'^author/invalid/$',
        views.AuthorInvalidView.as_view(),
        name='author-invalid'
    ),
    url(
        r'^author/template/$',
        views.AuthorTemplateView.as_view(),
        name='author-template'
    ),
    url(r'^book/$', views.BookView.as_view(), name='book-view'),
    url(r'^book/csv/$', views.BookCSVView.as_view(), name='book-csv-view'),
]

urlpatterns += router.urls
