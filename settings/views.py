from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from .models import Settings
from django.contrib.auth import get_user_model



class IndexView(TemplateView):
    template_name = 'settings/index.html'
    
    def get(self, request):
        user = get_user_model().objects.get(username=request.user.username)
        settings = Settings.objects.filter(user=user).first()
        
        if settings is not None:
            id = settings.github_id
            url = settings.repository_url
            return render(request, 'settings/index.html', {'github_id': id, 'repository_url': url})
        else:
            return render(request, 'settings/index.html')

class RegistrationView(TemplateView):
    template_name = 'settings/settings_registration.html'
    
    def post(self, request):
        if request.method == 'POST':
          user_instance = get_user_model().objects.get(username=request.user.username)
          
          user_name = user_instance
          id = request.POST.get('github_id')
          url = request.POST.get('repository_url')
          
          new_settings = Settings.objects.create(user=user_name, github_id=id, repository_url=url)
          new_settings.save()

          return redirect('settings:index')

class ChangeView(TemplateView):
    template_name = 'settings/settings_change.html'
    
    def post(self, request):
        if request.method == 'POST':
          user_instance = get_user_model().objects.get(username=request.user.username)
          change_settings = Settings.objects.filter(user=user_instance).first()
          
          change_settings.github_id = request.POST.get('github_id')
          change_settings.repository_url = request.POST.get('repository_url')
          
          change_settings.save()

          return redirect('settings:index')
        
class DevelopView(TemplateView):
    template_name = 'settings/develop.html'
    
    def get(self, request):
        user = get_user_model().objects.get(username=request.user.username)
        settings = Settings.objects.filter(user=user).first()
        
        if settings is not None:
            id = settings.github_id
            url = settings.repository_url
            checkbox = settings.isChecked
            if checkbox:
                return redirect('https://github.dev/' + settings.github_id + '/' + settings.repository_url)
            else:
                return render(request, 'settings/develop.html', {'github_id': id, 'repository_url': url})
        else:
            return render(request, 'settings/index.html')
        
    def post(self, request):
        if request.method == 'POST':
          user = get_user_model().objects.get(username=request.user.username)
          settings = Settings.objects.filter(user=user).first()
          
          checkbox_value = request.POST.get('checkbox')
          settings.isChecked = checkbox_value
          settings.isChecked = checkbox_value == 'on'
          settings.save()

          return redirect('https://github.dev/' + settings.github_id + '/' + settings.repository_url)