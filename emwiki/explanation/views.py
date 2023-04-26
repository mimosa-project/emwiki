import json
from natsort import humansorted
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Explanation
from django.views import generic
# from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.urls import reverse


class IndexView(TemplateView):
    template_name = 'explanation/index.html'


class CreateView(generic.CreateView):
    model = Explanation
    fields = ['title', 'text']


class ExplanationView(View):
    def get(self, title):
        explanations = humansorted(list(Explanation.objects.all()), key=lambda a: a.title)
        return JsonResponse({'index': [
            dict(id=explanation.id, title=explanation.title, text=explanation.text) for explanation in explanations
        ]})

    def post(self, request):
        post = json.loads(request.body)
        posted_id = post.get('id', None)
        posted_title = post.get('title', None)
        posted_text = post.get('text', None)
        errors = {}
        if not posted_title:
            errors[posted_title] = 'This field is required.'
            return JsonResponse({'errors': errors}, status=400)
        elif len(posted_title) > 200:
            errors[posted_title] = 'Title must be 200 characters or less.'
            return JsonResponse({'errors': errors}, status=400)
        elif Explanation.objects.exclude(id=posted_id).filter(title=posted_title).exists():
            errors[posted_title] = 'Title must be unique.'
            return JsonResponse({'errors': errors}, status=400)
        else:
            Explanation.objects.create(title=posted_title, text=posted_text)
            return redirect('explanation:index')


class DetailView(View):
    def get(self, request, title):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(title="temp")).replace('temp', ''),
        }
        return render(request, 'explanation/explanation_detail.html', context)


class UpdateView(View):
    def get(self, request, title):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(title="temp")).replace('temp', ''),
        }
        return render(request, 'explanation/explanation_change.html', context)

    def put(self, request, title):
        post = json.loads(request.body)
        updatedExplanation = Explanation.objects.get(title=title)
        updatedExplanation.text = post.get('text', None)
        updatedExplanation.save()
        return render(request, 'explanation/index.html')


class DeleteView(View):
    def get(self, request, title):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(title="temp")).replace('temp', ''),
        }
        return render(request, 'explanation/explanation_confirm_delete.html', context)

    def delete(self, request, title):
        deleteExplanation = Explanation.objects.get(title=title)
        deleteExplanation.delete()
        return render(request, 'explanation/index.html')
