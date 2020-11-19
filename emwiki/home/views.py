from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'


class AboutView(TemplateView):
    template_name = 'home/about.html'


class UsageView(TemplateView):
    template_name = 'home/usage.html'
