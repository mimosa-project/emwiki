from django.views.generic import TemplateView
from emwiki.settings import GRAPH_ELS_DIR
from emwiki.settings import BASE_DIR
from graph import create_graph
import json


class GraphView(TemplateView):
    template_name = 'graph/hierarchical_graph.html'

    def get_context_data(self, **kwargs):
        create_graph.main()
        context = super().get_context_data(**kwargs)
        with open(GRAPH_ELS_DIR + "/graph_attrs/dot_graph.json", "r") as f_in:
            graph_elements = json.load(f_in)
        context['graph_elements'] = graph_elements
        context['base'] = BASE_DIR
        return context