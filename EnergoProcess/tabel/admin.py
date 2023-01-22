from django.contrib import admin

from .models import *

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'electrical_safety_group')
    list_display_links = ('name',)
    search_fields = ('name',)

admin.site.register(Person, PersonAdmin)
