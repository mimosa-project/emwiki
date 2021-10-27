import json

from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView


class GraphView(TemplateView):
    template_name = 'graph/hierarchical_graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with open(settings.GRAPH_ELS_DIR + "/graph_attrs/dot_graph.json", "r") as f_in:
            graph_elements = json.load(f_in)
        context['graph_elements'] = graph_elements
        context['base_url'] = reverse('article:index')
        return context
