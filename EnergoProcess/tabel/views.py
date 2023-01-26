from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import *


menu = Person.objects.filter(position__contains='мастер')
def index(request):
    return TemplateResponse(request,  "tabel/index.htm", {'title': 'Табели бригад', 'menu': menu})

def about(request):
    return HttpResponse("Инструкция по заполнению табеля")

def tabel(request, tabel_id):
    return HttpResponse("Табель бригады")