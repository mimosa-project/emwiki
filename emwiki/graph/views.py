from django.views.generic import TemplateView


class GraphView(TemplateView):
    template_name = 'graph/graph.html'
