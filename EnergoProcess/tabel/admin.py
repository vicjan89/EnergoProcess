from django.contrib import admin

from .models import *


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

admin.site.register(Position, PositionAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'electrical_safety_group', 'subdivision')
    list_display_links = ('name',)
    search_fields = ('name',)

admin.site.register(Person, PersonAdmin)


class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('work_type',)

admin.site.register(WorkType, WorkTypeAdmin)


class TabelAdmin(admin.ModelAdmin):
    list_display = ('date_work', 'master', 'person', 'work_time', 'work_type', 'work_foreman',
                    'harmfulness', 'siding', 'combination', 'transferred')
    list_display_links = ('person',)
    search_fields = ('date_work', 'person')
    list_filter = ('date_work', 'master', 'person')


admin.site.register(Tabel, TabelAdmin)


class SubdivisionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


admin.site.register(Subdivision, SubdivisionAdmin)