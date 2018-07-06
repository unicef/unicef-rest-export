# UNICEF Rest Export

Django Rest Framework data export package that handles export/rendering to JSON, CSV, XLS, and HTML


## Installation

    pip install unicef-rest-export


## Setup

Add ``unicef_rest_export`` to ``INSTALLED_APPS`` in settings

    INSTALLED_APPS = [
        ...
        'unicef_rest_export',
    ]


## Usage

A sample model view;

    class AuthorView(ExportView):
        queryset = Author.objects.all()
        serializer_class = serializers.AuthorSerializer


A sample model viewset;

    class AuthorViewSet(ExportViewSet):
        queryset = Author.objects.all()
        serializer_class = serializers.AuthorSerializer


To override or limit the renderers allowed, add ``EXPORT_RENDERERS`` to settings.
The current default is;

    EXPORT_RENDERERS = (
        "unicef_rest_export.renderers.ExportHTMLRenderer",
        "unicef_rest_export.renderers.ExportCSVRenderer",
        "unicef_rest_export.renderers.ExportJSONRenderer",
        "unicef_rest_export.renderers.ExportExcelRenderer",
    )

The following is a sample of transforming data;

    class AuthorTransformView(ExportView):
        queryset = Author.objects.all()
        serializer_class = serializers.AuthorSerializer

        def transform_books(self, data):
            return [d["name"] for d in data]

        def transform_dataset(self, dataset):
            dataset.add_formatter("books", self.transform_books)
            return dataset


## Contributing

### Environment Setup

To install the necessary libraries

    $ make install


### Coding Standards

See [PEP 8 Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) for complete details on the coding standards.

To run checks on the code to ensure code is in compliance

    $ make lint


### Testing

Testing is important and tests are located in `tests/` directory and can be run with;

    $ make test

Coverage report is viewable in `build/coverage` directory, and can be generated with;


### Project Links

 - Continuos Integration - https://circleci.com/gh/unicef/unicef-rest-export/tree/develop
 - Source Code - https://github.com/unicef/unicef-rest-export


## Thanks to

[django-rest-pandas](https://github.com/wq/django-rest-pandas) as a lot of the code was borrowed from that package.
