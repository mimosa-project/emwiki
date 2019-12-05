from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from classes import Article
from classes import Comment


@ensure_csrf_cookie
def render_article(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/*.html'))
    file_list = [os.path.basename(absolute_path) for absolute_path in file_list]
    file_path = 'optional/start.html'
    context = {'file_path': file_path, 'file_list': file_list}
    return render(request, 'article/article.html', context)


def recieve_comment(request):
    file_name = request.POST.get('id', None)
    block = request.POST.get('block', None)
    block_order = request.POST.get("block_order", None)
    comment = request.POST.get('comment', None)
    article_name = file_name
    save_comment(article_name, {block: {int(block_order): comment}})
    return HttpResponse()


def send_comment(request, article_name):
    """send comments using JSON

    Args:
        request: HttpRequestObject
        article_name: article_name ex."abcmiz_0.html"

    Returns:
        A JSON like this

        {'comments': {
            'theorem': {1: "comment_text", 2: "comment_text", 3...},
            'definition': {1: "comment_text", 2: "comment_text", 3...},
            ...
        }
    """
    return_json = {'comments': {block: {} for block in TARGET_BLOCK}}
    comments_path = os.path.join(BASE_DIR, f'article/data/comment/{article_name}/')
    comments_path_list = glob.glob(comments_path + '*')
    for comment_path in comments_path_list:
        comment_name = os.path.basename(comment_path)
        block, block_order = comment_name.split("_")
        with open(comment_path, "r") as f:
            return_json['comments'][block][int(block_order)] = f.read()
    return JsonResponse(return_json)


def push_all_comment(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mml/*.miz'))
    file_list = [os.path.basename(absolute_path) for absolute_path in file_list]
    file_list = [os.path.splitext(extention_name)[0] for extention_name in file_list]
    print("push start")
    for article_name in file_list:
        embed_comment_to_file(article_name)
    print("push end")
    return HttpResponse()


def pull_all_comment(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mml/*.miz'))
    file_list = [os.path.basename(absolute_path) for absolute_path in file_list]
    file_list = [os.path.splitext(extention_name)[0] for extention_name in file_list]
    print("pull start")
    for article_name in file_list:
        extract_comment_to_file(article_name)
    print("pull end")
    return HttpResponse()
