from django.views.generic import TemplateView
from django.urls import reverse_lazy

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home/index.html'
