from django.http.response import JsonResponse

from .models import Symbol


def order_names(request):
    data = {
        'names': [
            symbol.name
            for symbol in Symbol.objects.all()
        ]
    }
    return JsonResponse(data)
