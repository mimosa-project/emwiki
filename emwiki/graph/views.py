from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView


class GraphView(TemplateView):
    template_name = 'graph/index.html'
    extra_context = {
        "context_for_js": {
            'article_names_uri': reverse_lazy('article:names'),
        }
    }

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.context_data['context_for_js']['article_base_uri'] = reverse(
            'article:index', kwargs=dict(name_or_filename="temp")).replace('temp', '')
        return response
