from accounts.forms import MyUserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import MyLoginForm


class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'


class Login(LoginView):
    form_class = MyLoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/logout.html'
