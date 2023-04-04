import json
from natsort import humansorted
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, Http404
from .models import Explanation
from django.views import generic
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import View
 
from django.urls import reverse, reverse_lazy



class IndexView(TemplateView):
    template_name = 'explanation/index.html'

class CreateView(generic.CreateView):
    model = Explanation
    fields = ['title', 'text']

class ExplanationView(View): 
    def get(self, request):
        explanations = humansorted(list(Explanation.objects.all()), key=lambda a: a.title)
        return JsonResponse({'index': [
            dict(id = explanation.id, title=explanation.title, text=explanation.text) for explanation in explanations
        ]})

    def post(self, request):
        post = json.loads(request.body)
        posted_title = post.get('title', None)
        posted_text = post.get('text', None)
        Explanation.objects.create(title=posted_title, text=posted_text)
        return redirect('explanation:index')

class DetailView(View):
    def get(self, request, id):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(id="temp")).replace('temp', ''),
        }
        return render(request, 'explanation/explanation_detail.html', context)

class UpdateView(View):
    def get(self, request, id):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(id="temp")).replace('temp', ''),
        }
        return render(request, 'explanation/explanation_change.html', context)
    
    def put(self, request, id):
        post = json.loads(request.body)
        explanations = humansorted(list(Explanation.objects.all()), key=lambda a: a.title)
        updatedExplanation = Explanation.objects.get(title=explanations[int(id)].title, text=explanations[int(id)].text)
        updatedExplanation.title = post.get('title', None)
        updatedExplanation.text = post.get('text', None)
        updatedExplanation.save()
        return render(request, 'explanation/index.html')
        
class DeleteView(View):
    def get(self, request, id):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(id="temp")).replace('temp', ''),
        }
        return render(request, 'explanation/explanation_confirm_delete.html', context)
    
    def delete(self, request, id):
        explanations = humansorted(list(Explanation.objects.all()), key=lambda a: a.title)
        deleteExplanation = Explanation.objects.get(title=explanations[int(id)].title, text=explanations[int(id)].text)
        deleteExplanation.delete()
        return render(request, 'explanation/index.html')

