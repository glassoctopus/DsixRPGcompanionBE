from django.middleware.csrf import get_token
from django.http import JsonResponse

def csrf_view(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})