from django.http.response import JsonResponse

from .models import Symbol


def order_symbol_names(request):
    data = {
        'symbol_names': [
            symbol.name
            for symbol in Symbol.objects.all()
        ]
    }
    return JsonResponse(data)
