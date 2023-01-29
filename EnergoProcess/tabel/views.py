from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import *


# menu = Person.objects.filter(position__contains='мастер')
menu = [{'title': 'Как заполнять табели', 'url_name': 'home'},
        {'title': 'Табели бригад', 'url_name': 'tabel'},
        {'title': 'Редактировать данные', 'url_name': 'admin:index'}
        ]
def index(request):
    return TemplateResponse(request,  "tabel/index.htm", {'title': 'Главная страница', 'menu': menu})


context = {'title': 'Табель бригады',
           'menu': menu,
           'brigades': list(set((i.supervisor for i in Brigades.objects.all())))}
def tabel(request):
    return TemplateResponse(request,  "tabel/tabel.htm", context=context)