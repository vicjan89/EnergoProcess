from django.db import models
from django.db.models import Q
from django.urls import reverse

class Position(models.Model):
    name = models.CharField(max_length=80, verbose_name='Должность/профессия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность/профессия'
        verbose_name_plural = 'Должность/профессия'
        ordering = ['name']


class Person(models.Model):
    name = models.CharField(max_length=40, verbose_name='Ф.И.О.')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, verbose_name='должность/профессия',
                                 blank=True, null=True)
    electrical_safety_group = models.CharField(max_length=3, verbose_name='группа по электробезопасности')
    subdivision = models.ForeignKey('Subdivision', on_delete = models.CASCADE, verbose_name='Подразделение', blank=True,
                                    null=True)
    personnel_number = models.IntegerField(verbose_name='табельный номер', blank=True, null=True)
    time_1234 = models.FloatField(verbose_name='Рабочее время по умолчанию Пн-Чт', blank=True, null=True, default=8.25)
    time_5 = models.FloatField(verbose_name='Рабочее время по умолчанию Пт', blank=True, null=True, default=7.0)
    combination_time = models.BooleanField(verbose_name='В табель бригады только совмещение', default=False, blank=True, null=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Работники'
        verbose_name_plural = 'Работники'
        ordering = ['name']


class WorkType(models.Model):
    work_type = models.CharField(max_length=4, verbose_name='Причина отсутствия')

    def __str__(self):
        return self.work_type

    class Meta:
        verbose_name = 'Причина отсутствия на работе'
        verbose_name_plural = 'Причины отсутствия на работе'
        ordering = ['work_type']

itr = Q(position=Position.objects.get(name='мастер')) | Q(position=Position.objects.get(name='старший мастер'))

class TabelRecord(models.Model):
    date_work = models.DateField(verbose_name='Дата')
    master = models.ForeignKey(Person, on_delete = models.CASCADE, verbose_name='Мастер', related_name='master', blank=True,
                               null=True, limit_choices_to=itr)
    person = models.ForeignKey(Person, on_delete = models.CASCADE, verbose_name='Работник', related_name='person')
    work_time = models.FloatField(verbose_name='Время работы', blank=True, null=True)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, verbose_name='Причина отсутствия', blank=True,
                                  null=True)
    work_foreman = models.BooleanField(verbose_name='Производитель', default=False)
    harmfulness = models.BooleanField(verbose_name='Вредность', default=True)
    siding = models.BooleanField(verbose_name='Разъезд', default=False)
    combination = models.FloatField(verbose_name='Совмещение', blank=True, null=True)
    transferred = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Передан', related_name='transferred',
                                    blank=True, null=True, limit_choices_to=itr)

    def __str__(self):
        out = str(self.date_work) + ' ' +  self.person.name + (str(self.work_time) if self.work_time else '') + (str(self.work_type) if self.work_type != None else '')
        return out

    class Meta:
        verbose_name = 'Табель рабочего времени'
        verbose_name_plural = 'Табель рабочего времени'
        ordering = ['date_work', 'person']


class Subdivision(models.Model):
    name = models.CharField(max_length=10, verbose_name='Подразделение', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['name']


class Brigades(models.Model):
    supervisor = models.ForeignKey(Person, on_delete=models.SET_NULL, verbose_name='руководитель бригады',
                                   related_name='supervisor', blank=True, null=True, limit_choices_to=itr)
    member = models.ForeignKey(Person, on_delete=models.SET_NULL, verbose_name='член бригады', related_name='member',
                               blank=True, null=True)

    def __str__(self):
        return self.supervisor.name + ' - ' + self.member.name

    class Meta:
        verbose_name = 'Состав бригады'
        verbose_name_plural = 'Состав бригады'
        ordering = ['supervisor']