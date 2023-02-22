import datetime
from calendar import Calendar
from django.template.response import TemplateResponse
from django.views.generic import DetailView

from .models import *


menu = [{'title': 'Как заполнять табели', 'url_name': 'home'},
        {'title': 'Табели бригад', 'url_name': 'tabel'},
        {'title': 'Табель подразделения', 'url_name': 'tabel_total'},
        {'title': 'Редактировать данные', 'url_name': 'admin:index'}
        ]
def index(request):
    return TemplateResponse(request,  "tabel/index.htm", {'title': 'Главная страница', 'menu': menu})



def check_errors(month: int, year: int):
    errors = []
    tabel_filtred = TabelRecord.objects.filter(date_work__year=year).filter(date_work__month=month).filter(transferred=None)
    records = [(record.date_work, record.person) for record in tabel_filtred]
    workers = Person.objects.all()
    boss = Person.objects.get(position__name='начальник')
    not_work_type = [wt for wt in WorkType.objects.all() if wt.work_type in ('О', 'Б', 'А', 'Ук', 'У')]
    master_for_worker = {i.member.name: i.supervisor for i in Brigades.objects.all()}
    cal = Calendar()
    for dt in cal.itermonthdates(year=year, month=month):
        if dt.month == month:
            for worker in workers:
                num = records.count((dt, worker))
                if num == 0:
                    errors.append((dt, worker, master_for_worker.get(worker.name, boss), ' не внесён в табель'))
                elif num > 1:
                    tf = TabelRecord.objects.filter(date_work=dt).filter(person=worker).filter(transferred=None)
                    text_add = ' '.join(i.master.name for i in tf)
                    for t in tf:
                        text = f' внесён в табель {num} раза: ' + text_add
                        errors.append((dt, worker, t.master, text))
    for record in tabel_filtred:
        if record.work_type in not_work_type:
            if record.work_time:
                errors.append((record.date_work, record.person, record.master, ' установлено рабочее время для отсутствующего работника'))
            if record.work_foreman:
                errors.append((record.date_work, record.person, record.master, ' установлена доплата за производителя отсутствующему работнику'))
            if record.harmfulness:
                errors.append((record.date_work, record.person, record.master, ' установлена вредность отсутствующему работнику'))
            if record.siding:
                errors.append((record.date_work, record.person, record.master, ' установлен разъезд отсутствующему работнику'))
            if record.transferred:
                errors.append((record.date_work, record.person, record.master, ' установлено совмещение отсутствующему работнику'))
        if (record.work_time and ((0 <= record.date_work.weekday() <= 3) and record.work_time < record.person.time_1234 or
                (record.date_work.weekday() == 4) and record.work_time < record.person.time_5) and record.harmfulness):
            errors.append((record.date_work, record.person, record.master, ' установлена вредность при неполном рабочем дне'))

    return errors

def fill_by_default(person: Person, master: Person, year: int, month: int, tabel_record: TabelRecord, harmfulness):
    cal = Calendar()
    work_type_day_off = WorkType.objects.get(work_type='В')
    for dt in cal.itermonthdates(year=year, month=month):
        work_type = None
        if dt.month == month:
            if 0 <= dt.weekday() <= 3:
                work_time = person.time_1234
            elif dt.weekday() == 4:
                work_time = person.time_5
            else:
                work_time = None
                work_type = work_type_day_off
            tabel_record.objects.create(date_work=dt, master=master, person=person, work_time=work_time,
                                       work_type=work_type, harmfulness=harmfulness)

def tabel(request):
    context = {'title': 'Табель бригады',
               'menu': menu,
               'brigades': list(set((i.supervisor for i in Brigades.objects.all()))),
               'person': Person}

    month_by_number = {1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель', 5: 'май', 6: 'июнь',
                       7: 'июль', 8: 'август', 9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'}

    supervisor_id = request.POST.get("supervisor_id", 1)
    month = int(request.POST.get("month", datetime.datetime.now().month))
    year = int(request.POST.get("year", datetime.datetime.now().year))
    context['month_name'] = month_by_number[month]
    context['month'] = month
    context['year'] = year
    context['supervisor'] = Person.objects.get(pk=supervisor_id)
    brigada = [i.member for i in Brigades.objects.filter(supervisor=supervisor_id)]
    context['brigada'] = brigada
    master = Person.objects.get(pk=int(supervisor_id))
    if not TabelRecord.objects.filter(master=supervisor_id).filter(date_work__month=month):
        cal = Calendar()
        for dt in cal.itermonthdates(year=year, month=month):
            work_type = None
            if dt.month == month:
                for m in brigada:
                    if 0 <= dt.weekday() <= 3:
                        work_time = m.time_1234
                    elif dt.weekday() == 4:
                        work_time = m.time_5
                    else:
                        work_time = None
                        work_type = WorkType.objects.get(work_type='В')
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
        tabel_dict[b.name].append(True)
    for i in tabel_filtred:
        if i.person.name not in tabel_dict:
            tabel_dict[i.person.name] = [' ' for i in range(31)]
            tabel_dict[i.person.name].append(i.person.position)
            tabel_dict[i.person.name].append(i.person.personnel_number)
            tabel_dict[i.person.name].append(0.0)
            tabel_dict[i.person.name].append(False)
        if i.person.combination_time:
            work_text = str(i.combination) if i.combination else ''
            tabel_dict[i.person.name][33] += i.combination if i.combination else 0.0
        else:
            work_text = str(i.work_time) if i.work_time else ''
            tabel_dict[i.person.name][33] += i.work_time if i.work_time else 0.0
        work_text += ' ' + (str(i.work_type) if i.work_type != None else '')
        tabel_dict[i.person.name][i.date_work.day-1] = work_text


    for key, value in tabel_dict.items():
        tabel_row =[key]
        tabel_row.extend(value)
        total += value[33]
        context['tabel'].append(tabel_row)
    context['total'] = total
    context['errors'] = check_errors(month, year)
    return TemplateResponse(request, "tabel/tabel.htm", context=context)

def tabel_total(request):
    context = {'title': 'Табель подразделения',
               'menu': menu}

    month_by_number = {1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель', 5: 'май', 6: 'июнь',
                       7: 'июль', 8: 'август', 9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'}

    month = int(request.POST.get("month", datetime.datetime.now().month))
    year = int(request.POST.get("year", datetime.datetime.now().year))
    context['month_name'] = month_by_number[month]
    context['month'] = month
    context['year'] = year
    tabel_filtred = TabelRecord.objects.filter(date_work__month=month).filter(transferred=None).filter(person__position__name='начальник')
    boss = Person.objects.get(position__name='начальник')
    if not tabel_filtred:
        fill_by_default(boss, boss, year, month, TabelRecord, False)
    tabel_filtred = TabelRecord.objects.filter(date_work__month=month).filter(transferred=None).filter(person__position__name='заместитель начальника')
    if not tabel_filtred:
        fill_by_default(Person.objects.get(position__name='заместитель начальника'), boss, year, month, TabelRecord, False)
    tabel_filtred = TabelRecord.objects.filter(date_work__month=month).filter(transferred=None).filter(person__position__name='инженер')
    if not tabel_filtred:
        fill_by_default(Person.objects.get(position__name='инженер'), boss, year, month, TabelRecord, False)
    tabel_filtred = TabelRecord.objects.filter(date_work__month=month).filter(transferred=None).filter(person__position__name='техник (по документации)')
    if not tabel_filtred:
        fill_by_default(Person.objects.get(position__name='техник (по документации)'), boss, year, month, TabelRecord, False)
    tabel_filtred = TabelRecord.objects.filter(date_work__month=month).filter(transferred=None)
    context['tabel'] = []
    tabel_dict = dict()
    total = 0.0
    workers = Person.objects.all()
    for worker in workers:
        tabel_dict[worker.name] = [' ' for i in range(31)]
        tabel_dict[worker.name].append(worker.position) #32
        tabel_dict[worker.name].append(worker.personnel_number) #33
        tabel_dict[worker.name].append(0.0) #34 итого времени
        tabel_dict[worker.name].append(0)  # 35 итого дней
        tabel_dict[worker.name].append(0.0)  # 36 совмещение
        tabel_dict[worker.name].append(0)  # 37 разъезды
    for record in tabel_filtred:
        work_text = ''
        if record.work_time:
            work_text += f'{record.work_time}'
        if record.work_type:
            work_text += f'{record.work_type}'
        if record.combination:
            work_text += f' ДС{record.combination}'
        if record.harmfulness and record.work_time:
            work_text += f' ВР{record.work_time}'
        if record.siding:
            work_text += f' ОР'
        if record.work_foreman:
            work_text += f' ПВР{record.work_time}'
        tabel_dict[record.person.name][record.date_work.day-1] = work_text
        tabel_dict[record.person.name][33] += record.work_time if record.work_time else 0.0
        tabel_dict[record.person.name][34] += 1 if record.work_time else 0
        tabel_dict[record.person.name][35] += record.combination if record.combination else 0.0
        tabel_dict[record.person.name][36] += record.siding

    for key, value in tabel_dict.items():
        tabel_row =[key]
        tabel_row.extend(value)
        total += value[33]
        context['tabel'].append(tabel_row)
    context['total'] = total
    context['errors'] = check_errors(month, year)
    return TemplateResponse(request, "tabel/tabel_total.htm", context=context)