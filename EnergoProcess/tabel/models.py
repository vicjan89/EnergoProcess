from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=40, verbose_name='Ф.И.О.')
    position = models.CharField(max_length=40, verbose_name='должность/профессия')
    electrical_safety_group = models.CharField(max_length=3, verbose_name='группа по электробезопасности')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Работники'
        verbose_name_plural = 'Работники'
        ordering = ['name']