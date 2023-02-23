import datetime

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from .models import *

admin.site.site_header = 'Табели СРЗАИ'

class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

admin.site.register(Position, PositionAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('personnel_number', 'name', 'position', 'electrical_safety_group', 'subdivision', 'time_1234', 'time_5', 'combination_time')
    list_display_links = ('name',)
    search_fields = ('name',)

admin.site.register(Person, PersonAdmin)


class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('work_type',)

admin.site.register(WorkType, WorkTypeAdmin)

@admin.action(description='Работник на больничном')
def make_sick(modeladmin, request, queryset):
    queryset.update(work_time=None, work_type=WorkType.objects.get(work_type='Б'), work_foreman=False, harmfulness=False,
                    siding=False, combination=None, transferred=None)

@admin.action(description='Работник в отпуске')
def make_on_vacation(modeladmin, request, queryset):
    queryset.update(work_time=None, work_type=WorkType.objects.get(work_type='О'), work_foreman=False, harmfulness=False,
                    siding=False, combination=None, transferred=None)

class ScrapeStatusFilter(SimpleListFilter):
    title = "декады месяца"  # a label for our filter
    parameter_name = "decade"  # you can put anything here

    def lookups(self, request, model_admin):
        return (
            ('d_1', _('1 декада')),
            ('d_2', _('2 декада')),
            ('d_3', _('3 декада')),
        )

    def queryset(self, request, queryset):
        if self.value() == "d_1":
            return queryset.filter(date_work__month=datetime.date.today().month).filter(date_work__day__lte=10)
        if self.value() == "d_2":
            return queryset.filter(date_work__month=datetime.date.today().month).filter(date_work__day__lte=20).filter(date_work__day__gt=10)
        if self.value() == "d_3":
            return queryset.filter(date_work__month=datetime.date.today().month).filter(date_work__day__gt=20)

class TabelRecordAdmin(admin.ModelAdmin):
    list_display = ('date_work', 'person', 'work_time', 'work_type', 'work_foreman',
                    'harmfulness', 'siding', 'transferred', 'master',)
    list_display_links = ('date_work',)
    list_editable = ('master', 'person', 'work_time', 'work_type', 'work_foreman',
                    'harmfulness', 'siding', 'transferred')
    search_fields = ('date_work', 'person')
    list_filter = ('date_work', ScrapeStatusFilter, 'master', 'person')
    actions = [make_sick, make_on_vacation]
    save_as = True


admin.site.register(TabelRecord, TabelRecordAdmin)


class SubdivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


admin.site.register(Subdivision, SubdivisionAdmin)

class BrigadesAdmin(admin.ModelAdmin):
    list_display = ('supervisor', 'member')
    list_display_links = ('supervisor', 'member')

admin.site.register(Brigades, BrigadesAdmin)