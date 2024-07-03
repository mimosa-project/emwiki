import json
import re
from natsort import humansorted
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from .models import Explanation
from article.models import Article
from django.core.exceptions import ValidationError
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


extra_context = {
    "context_for_js": {
        'base_uri': reverse_lazy('explanation:index'),
        'titles_uri': reverse_lazy('explanation:titles'),
        'article_base_uri': reverse_lazy('article:names'),
        'article_html_base_uri': reverse_lazy('article:htmls'),
        'article_index_uri': reverse_lazy('article:index'),
        'article_proof_uri': reverse_lazy('article:proofs'),
        'article_ref_uri': reverse_lazy('article:refs'),
    }
}


class IndexView(TemplateView):
    template_name = 'explanation/index.html'
    extra_context = {
        "context_for_js": {
            'base_uri': reverse_lazy('explanation:index'),
            'titles_uri': reverse_lazy('explanation:titles'),
        }
    }


class CreateView(generic.CreateView):
    model = Explanation
    fields = ['title', 'text', 'author', 'created_at', 'updated_at']
    extra_context = {
        'context_for_js': {
            'base_uri': reverse_lazy('explanation:index'),
            'titles_uri': reverse_lazy('explanation:titles'),
            'explanation_uri': reverse_lazy('explanation:explanation'),
            'article_names_uri': reverse_lazy('article:names'),
            'article_html_base_uri': reverse_lazy('article:htmls'),
        }
    }


class ExplanationTitleView(View):
    def get(self, request):
        explanations = humansorted(list(Explanation.objects.all()), key=lambda a: a.title)
        return JsonResponse({'index': [
            dict(id=explanation.id, title=explanation.title) for explanation in explanations
        ]})


class ExplanationView(View):
    def get(self, request, title=None):
        if 'title' in request.GET:
            selectedExplanation = get_object_or_404(Explanation, title=request.GET.get('title'))
            selected_text = selectedExplanation.text
            selected_preview = selectedExplanation.preview
            return JsonResponse({'text': selected_text, 'preview': selected_preview})

        elif 'article_name' in request.GET:
            explanations = Explanation.objects.filter(related_articles=request.GET.get('article_name'))
            related_titles = []
            for explanation in explanations:
                related_titles.append(explanation.title)
            return JsonResponse({"related_documents": related_titles})

        else:
            explanations = humansorted(list(Explanation.objects.all()), key=lambda a: a.title)
            return JsonResponse({'explanation': [
                dict(id=explanation.id, title=explanation.title, text=explanation.text) for explanation in explanations
            ]})

    def validate_explanation_title(self, blog_id, title):
        if not title:
            raise ValidationError('This field is required.')

        if len(title) > 200:
            raise ValidationError('Title must be 200 characters or less.')

        if Explanation.objects.exclude(id=blog_id).filter(title=title).exists():
            raise ValidationError('Title must be unique.')

    @method_decorator(login_required)
    def post(self, request):
        post = json.loads(request.body)
        posted_id = post.get('id', None)
        posted_title = post.get('title', None)
        posted_text = post.get('text', None)
        posted_preview = post.get('preview', None)

        if request.user.is_authenticated:
            username = request.user.username
            User = get_user_model()
            user = User.objects.get(username=username)

        try:
            self.validate_explanation_title(posted_id, posted_title)
        except ValidationError as e:
            errors = e.messages[0]
            return JsonResponse({'errors': errors}, status=400)

        createExplanation = Explanation.objects.create(title=posted_title, text=posted_text, preview=posted_preview, author=user)

        pattern = r"embed\(/article/([^#]+)#.*\)"
        article_names = re.findall(pattern, posted_text)
        for article_name in article_names:
            try:
                article = get_object_or_404(Article, name=article_name)
                createExplanation.related_articles.add(article)
            except Http404:
                print(f"Article with name {article_name} not found.")

        createExplanation.commit_explanation_creates()

        return redirect('explanation:index')


class DetailView(View):
    def get(self, request, title):
        explanations = humansorted(list(Explanation.objects.all()), key=lambda a: a.title)
        title_exists = any(explanation.title == title for explanation in explanations)
        if title_exists:
            context = dict()
            context["context_for_js"] = {
                'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(title="temp")).replace('temp', ''),
                'base_uri': reverse_lazy('explanation:index'),
                'titles_uri': reverse_lazy('explanation:titles'),
                'explanation_uri': reverse_lazy('explanation:explanation'),
            }
            return render(request, 'explanation/explanation_detail.html', context)
        else:
            target_url = reverse('article:index', kwargs={'name_or_filename': title})
            return redirect(target_url)


class UpdateView(View):
    def get(self, request, title):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(title="temp")).replace('temp', ''),
            'base_uri': reverse_lazy('explanation:index'),
            'titles_uri': reverse_lazy('explanation:titles'),
            'explanation_uri': reverse_lazy('explanation:explanation'),
            'article_html_base_uri': reverse_lazy('article:htmls'),
        }
        return render(request, 'explanation/explanation_change.html', context)

    def put(self, request, title):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        post = json.loads(request.body)
        updatedExplanation = Explanation.objects.get(title=title)
        User = get_user_model()
        username = request.user.username
        update_author = User.objects.get(username=username)
        updatedExplanation.text = post.get('text', None)
        updatedExplanation.preview = post.get('preview', None)
        updatedExplanation.author = update_author

        updatedExplanation.related_articles.clear()

        pattern = r"embed\(/article/([^#]+)#.*\)"
        article_names = re.findall(pattern, updatedExplanation.text)
        for article_name in article_names:
            try:
                article = get_object_or_404(Article, name=article_name)
                updatedExplanation.related_articles.add(article)
            except Http404:
                print(f"Article with name {article_name} not found.")

        updatedExplanation.save()
        updatedExplanation.commit_explanation_changes()
        return render(request, 'explanation/index.html')


class DeleteView(View):
    def get(self, request, title):
        context = dict()
        context["context_for_js"] = {
            'explanation_detail_uri': reverse('explanation:detail', kwargs=dict(title="temp")).replace('temp', ''),
            'base_uri': reverse_lazy('explanation:index'),
            'titles_uri': reverse_lazy('explanation:titles'),
            'explanation_uri': reverse_lazy('explanation:explanation'),
        }
        return render(request, 'explanation/explanation_confirm_delete.html', context)

    def delete(self, request, title):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        deleteExplanation = Explanation.objects.get(title=title)
        deleteExplanation.delete()
        return render(request, 'explanation/index.html')


class ArticleView(View):
    def get(self, request, name_or_filename):
        target_url = reverse('article:index', kwargs={'name_or_filename': name_or_filename})
        return redirect(target_url)


class ProofView(View):
    def get(self, request, article_name, proof_name):
        target_url = reverse('article:proofs', kwargs={'article_name': article_name, 'proof_name': proof_name})
        return redirect(target_url)


class RefView(View):
    def get(self, request, article_name, ref_name):
        target_url = reverse('article:refs', kwargs={'article_name': article_name, 'ref_name': ref_name})
        return redirect(target_url)


class Detail_ProofView(View):
    def get(self, request, article_name, proof_name):
        target_url = reverse('article:proofs', kwargs={'article_name': article_name, 'proof_name': proof_name})
        return redirect(target_url)


class Detail_RefView(View):
    def get(self, request, article_name, ref_name):
        target_url = reverse('article:refs', kwargs={'article_name': article_name, 'ref_name': ref_name})
        return redirect(target_url)


class Update_ArticleView(View):
    def get(self, request, name_or_filename, title):
        target_url = reverse('article:index', kwargs={'name_or_filename': name_or_filename})
        return redirect(target_url)


class Update_ProofView(View):
    def get(self, request, article_name, proof_name, title):
        target_url = reverse('article:proofs', kwargs={'article_name': article_name, 'proof_name': proof_name})
        return redirect(target_url)


class Update_RefView(View):
    def get(self, request, article_name, ref_name, title):
        target_url = reverse('article:refs', kwargs={'article_name': article_name, 'ref_name': ref_name})
        return redirect(target_url)