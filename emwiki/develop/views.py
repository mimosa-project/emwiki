from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from .models import Develop
from django.contrib.auth import get_user_model


class IndexView(TemplateView):
    template_name = 'develop/index.html'

    def get(self, request):
        user = get_user_model().objects.get(username=request.user.username)
        settings = Develop.objects.filter(user=user).first()

        if settings is not None:
            id = settings.github_id
            repository_name = settings.repository_name
            return render(request, 'develop/index.html', {'github_id': id, 'repository_name': repository_name})
        else:
            return render(request, 'develop/index.html')


class RegistrationView(TemplateView):
    template_name = 'develop/settings_registration.html'

    def post(self, request):
        if request.method == 'POST':
            user_name = get_user_model().objects.get(username=request.user.username)
            id = request.POST.get('github_id')
            repository_name = request.POST.get('repository_name')
            new_settings = Develop.objects.create(user=user_name, github_id=id, repository_name=repository_name)
            new_settings.save()

            return redirect('develop:index')


class ChangeView(TemplateView):
    template_name = 'develop/settings_change.html'

    def get(self, request):
        user = get_user_model().objects.get(username=request.user.username)
        settings = Develop.objects.filter(user=user).first()

        return render(request, 'develop/settings_change.html', {'settings': settings})

    def post(self, request):
        if request.method == 'POST':
            change_settings = Develop.objects.filter(user=get_user_model().objects.get(username=request.user.username)).first()
            change_settings.github_id = request.POST.get('github_id')
            change_settings.repository_name = request.POST.get('repository_name')
            change_settings.save()

            return redirect('develop:index')


class DevelopView(TemplateView):
    template_name = 'develop/develop.html'

    def get(self, request):
        settings = Develop.objects.filter(user=get_user_model().objects.get(username=request.user.username)).first()

        if settings is not None:
            id = settings.github_id
            repository_name = settings.repository_name

            return render(request, 'develop/develop.html', {'github_id': id, 'repository_name': repository_name})
        else:
            return render(request, 'develop/develop.html')
