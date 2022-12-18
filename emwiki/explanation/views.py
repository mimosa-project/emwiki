import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from .models import Explanation
from django.views import generic
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import View
 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class IndexView(TemplateView):
    template_name = 'explanation/index.html'

class CreateView(generic.CreateView):
    model = Explanation
    fields = ['title', 'text']

class ExplanationView(View): 
    # def get(self, request):
    #     explanations = Explanation.objects.title()
    #     return HttpResponse({'explanations':explanations})

    def post(self, request):
        post = json.loads(request.body)
        posted_title = post.get('title', None)
        posted_text = post.get('text', None)
        Explanation.objects.create(title=posted_title, text=posted_text)
        return HttpResponse(posted_title, posted_text)

class DetailView(generic.DetailView): 
    model = Explanation  # pk(primary key)はurls.pyで指定しているのでここではmodelを呼び出すだけで済む
    
class UpdateView(generic.UpdateView):
    model = Explanation
    fields = ['title', 'text']
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
 
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
 
        return super(UpdateView, self).dispatch(request, *args, **kwargs)
    success_url = reverse_lazy('explanation:detail')
    
class DeleteView(generic.DeleteView):
    model = Explanation
    success_url = reverse_lazy('explanation:index')

