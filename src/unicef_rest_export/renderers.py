import os
from io import StringIO
from tempfile import mkstemp

from rest_framework import status
from rest_framework.renderers import BaseRenderer, TemplateHTMLRenderer
from tablib import Dataset

RESPONSE_ERROR = (
    "Response data is a %s, not a Dataset! "
    "Did you extend ExportMixin?"
)


class ExportBaseRenderer(BaseRenderer):
    """Renders Datasets using their built in export implementation.
    Only works with serializers that return Datasets as their data object.
    Uses a StringIO to capture the output of dataset.export('[format]')
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'response' in renderer_context:
            status_code = renderer_context['response'].status_code
            if not status.is_success(status_code):
                return "Error: %s" % data.get('detail', status_code)

        if not isinstance(data, Dataset):
            raise Exception(
                RESPONSE_ERROR % type(data).__name__
            )

        self.init_output()
        args = self.get_export_args(data)
        kwargs = self.get_export_kwargs(data, renderer_context)
        self.render_dataset(data, *args, **kwargs)
        return self.get_output()

    def render_dataset(self, data, *args, **kwargs):
        self.output.write(data.export(self.format))

    def init_output(self):
        self.output = StringIO()

    def get_output(self):
        return self.output.getvalue()

    def get_export_args(self, data):
        return [self.output]

    def get_export_kwargs(self, data, renderer_context):
        return {}


class ExportFileRenderer(ExportBaseRenderer):
    """Renderer for output formats that absolutely must use a file
    (i.e. Excel)
    """
    def init_output(self):
        file, filename = mkstemp(suffix='.' + self.format)
        self.filename = filename
        os.close(file)

    def render_dataset(self, data, *args, **kwargs):
        with open(self.filename, "wb") as fp:
            fp.write(data.export(self.format))

    def get_export_args(self, data):
        return [self.filename]

    def get_output(self):
        file = open(self.filename, 'rb')
        result = file.read()
        file.close()
        os.unlink(self.filename)
        return result


class ExportHTMLRenderer(TemplateHTMLRenderer, ExportBaseRenderer):
    media_type = "text/html"
    format = "html"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        table = ExportBaseRenderer.render(
            self, data, accepted_media_type, renderer_context,
        )

        return TemplateHTMLRenderer.render(
            self, {'table': table}, accepted_media_type, renderer_context,
        )

    def get_template_context(self, data, renderer_context):
        view = renderer_context['view']
        request = renderer_context['request']

        data['name'] = view.get_view_name()
        data['description'] = view.get_view_description(html=True)
        data['url'] = request.path.replace('.html', '')
        full_path = request.get_full_path()
        if '?' in full_path:
            data['url_params'] = full_path[full_path.index('?'):]
        data['available_formats'] = [
            cls.format for cls in view.renderer_classes
            if cls.format != 'html'
        ]

        if hasattr(view, 'get_template_context'):
            data.update(view.get_template_context(data))

        return data

    def get_export_kwargs(self, data, renderer_context):
        return {
            'classes': 'ui-table table-stripe',
            'na_rep': '',
        }


class ExportCSVRenderer(ExportBaseRenderer):
    """
    Renders data frame as CSV
    """
    media_type = "text/csv"
    format = "csv"

    def get_export_kwargs(self, data, renderer_context):
        return {'encoding': self.charset}


class ExportJSONRenderer(ExportBaseRenderer):
    """Renders dataset as JSON"""
    media_type = "application/json"
    format = "json"

    date_format_choices = {'epoch', 'iso'}
    default_date_format = 'iso'

    def get_export_kwargs(self, data, renderer_context):
        request = renderer_context['request']

        date_format = request.GET.get('date_format', '')
        if date_format not in self.date_format_choices:
            date_format = self.default_date_format

        return {
            'date_format': date_format,
        }


class ExportExcelRenderer(ExportFileRenderer):
    """Renders dataset as Excel (.xlsx)"""
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # noqa
    format = "xls"
