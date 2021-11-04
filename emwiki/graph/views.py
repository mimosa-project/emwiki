from django.urls import reverse
from django.views.generic import TemplateView


class GraphView(TemplateView):
    template_name = 'graph/index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context["context_for_js"] = {
            'article_names_uri': reverse('article:names')
        }
        return context
