from django.db import models
from django.db.models import Q

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Работники'
        verbose_name_plural = 'Работники'
        ordering = ['name']

class Brigades(models.Model):
    supervisor = models.ForeignKey(Person, on_delete=models.SET_NULL, verbose_name='руководитель бригады',
                                   related_name='supervisor', null=True)
    member = models.ForeignKey(Person, on_delete=models.SET_NULL, verbose_name='член бригады',
                               related_name='member', null=True)

    def __str__(self):
        return self.supervisor.name + '-' + self.member.name

    class Meta:
        verbose_name = 'Состав бригады'
        verbose_name_plural = 'Состав бригады'
        ordering = ['supervisor']


class WorkType(models.Model):
    work_type = models.CharField(max_length=4, verbose_name='Причина отсутствия')

    def __str__(self):
        return self.work_type

    class Meta:
        verbose_name = 'Причина отсутствия на работе'
        verbose_name_plural = 'Причины отсутствия на работе'
        ordering = ['work_type']

class Tabel(models.Model):
    date_work = models.DateField(verbose_name='Дата')
    master = models.ForeignKey(Person, on_delete = models.CASCADE, verbose_name='Мастер', related_name='master',
                               null=True, limit_choices_to=Q(position='мастер') | Q(position='старший мастер'))
    person = models.ForeignKey(Person, on_delete = models.CASCADE, verbose_name='Работник', related_name='person',
                               limit_choices_to=Q())
    work_time = models.FloatField(verbose_name='Время работы', blank=True, null=True)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, verbose_name='Причина отсутствия', blank=True, null=True)
    work_foreman = models.BooleanField(verbose_name='Производитель', default=False)
    harmfulness = models.BooleanField(verbose_name='Вредность', default=False)
    siding = models.BooleanField(verbose_name='Разъезд', default=False)
    combination = models.FloatField(verbose_name='Совмещение', blank=True, null=True)
    transferred = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Передан',
                                    related_name='transferred', blank=True, null=True)

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