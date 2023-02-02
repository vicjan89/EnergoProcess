from calendar import Calendar
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

month_by_number = {'1': 'январь', '2': 'февраль', '3': 'март', '4': 'апрель', '5': 'май', '6': 'июнь',
                   '7': 'июль', '8': 'август', '9': 'сентябрь', '10': 'октябрь', '11': 'ноябрь', '12': 'декабрь'}
def tabel(request):
    supervisor_id = request.POST.get("supervisor_id", 1)
    month = request.POST.get("month", '1')
    year = request.POST.get("year", '2023')
    context['month'] = month_by_number[month]
    context['supervisor'] = Person.objects.get(pk=supervisor_id)
    brigada = [i.member for i in Brigades.objects.filter(supervisor=supervisor_id)]
    master = Person.objects.get(pk=int(supervisor_id))
    if not TabelRecord.objects.filter(master=supervisor_id).filter(date_work__month=month):
        mnth = int(month)
        cal = Calendar()
        for dt in cal.itermonthdates(year=int(year), month=mnth):
            work_type = None
            if dt.month == mnth:
                if 0 <= dt.weekday() <= 3:
                    work_time = 8.25
                elif dt.weekday() == 4:
                    work_time = 7.0
                else:
                    work_time = None
                    work_type = WorkType.objects.get(work_type='В')
                for m in brigada:
                    TabelRecord.objects.create(date_work=dt, master=master, person=m, work_time=work_time,
                                               work_type=work_type, harmfulness=True)
    tabel_filtred = TabelRecord.objects.filter(master=supervisor_id).filter(date_work__month=month).filter(transferred=None)
    context['tabel'] = []
    tabel_dict = dict()
    total = 0.0
    for b in brigada:
        tabel_dict[b.name] = [' ' for i in range(31)]
        tabel_dict[b.name].append(b.position)
        tabel_dict[b.name].append(b.personnel_number)
        tabel_dict[b.name].append(0.0)
    for i in tabel_filtred:
        if i.person.name not in tabel_dict:
            tabel_dict[i.person.name] = [' ' for i in range(31)]
            tabel_dict[i.person.name].append(i.person.position)
            tabel_dict[i.person.name].append(i.person.personnel_number)
            tabel_dict[i.person.name].append(0.0)
        tabel_dict[i.person.name][i.date_work.day-1] = (str(i.work_time) if i.work_time
                                                        else '') + ' ' + (str(i.work_type) if i.work_type != None else '')
        tabel_dict[i.person.name][33] += i.work_time if i.work_time else 0.0
    for key, value in tabel_dict.items():
        tabel_row =[key]
        tabel_row.extend(value)
        total += value[33]
        context['tabel'].append(tabel_row)
    context['total'] = total
    return TemplateResponse(request, "tabel/tabel.htm", context=context)