from django.contrib import admin

from .models import *


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

admin.site.register(Position, PositionAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('personnel_number', 'name', 'position', 'electrical_safety_group', 'subdivision')
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

class TabelRecordAdmin(admin.ModelAdmin):
    list_display = ('date_work', 'master', 'person', 'work_time', 'work_type', 'work_foreman',
                    'harmfulness', 'siding')
    list_display_links = ('date_work',)
    list_editable = ('master', 'person', 'work_time', 'work_type', 'work_foreman',
                    'harmfulness', 'siding')
    search_fields = ('date_work', 'person')
    list_filter = ('date_work', 'master', 'person')
    actions = [make_sick]

admin.site.register(TabelRecord, TabelRecordAdmin)


class SubdivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


admin.site.register(Subdivision, SubdivisionAdmin)

class BrigadesAdmin(admin.ModelAdmin):
    list_display = ('supervisor', 'member')
    list_display_links = ('supervisor', 'member')

admin.site.register(Brigades, BrigadesAdmin)