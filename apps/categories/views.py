import json
from django.http import HttpResponse
from .models import Category


def list(request):
    categories = Category.objects.all()

    data = []
    for c in categories:
        data.append({'label': c.name, 'value': c.slug})

    return HttpResponse(json.JSONEncoder().encode(data),
                        content_type='application/json')
