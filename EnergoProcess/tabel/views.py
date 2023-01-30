from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import *


menu = [{'title': 'Как заполнять табели', 'url_name': 'home'},
        {'title': 'Табели бригад', 'url_name': 'tabel'},
        {'title': 'Редактировать данные', 'url_name': 'admin:index'}
        ]
def index(request):
    return TemplateResponse(request,  "tabel/index.htm", {'title': 'Главная страница', 'menu': menu})


context = {'title': 'Табель бригады',
           'menu': menu,
           'brigades': list(set((i.supervisor for i in Brigades.objects.all()))),
           'person': Person}

def tabel(request, supervisor_id, month):
    context['supervisor'] = Person.objects.get(pk=supervisor_id)
    brigada = [i.member for i in Brigades.objects.filter(supervisor=supervisor_id)]
    tabel_filtred = TabelRecord.objects.filter(master=supervisor_id).filter(date_work__month=month).filter(transferred=None)
    context['tabel'] = []
    tabel_dict = dict()
    for b in brigada:
        tabel_dict[b.name] = ['' for i in range(31)]
    for i in tabel_filtred:
        tabel_dict[i.person.name][i.date_work.month] = str(i)
    for key, value in tabel_dict.items():
        tabel_row =[key]
        for i in value:
            tabel_row.append(i)
        context['tabel'].append(tabel_row)
    return TemplateResponse(request, "tabel/tabel.htm", context=context)