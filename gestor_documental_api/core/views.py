from django.http import JsonResponse

def health(request):
    return JsonResponse({'status': 'ok', 'service': 'gestor-documental-api', 'version': '0.1.0'})
