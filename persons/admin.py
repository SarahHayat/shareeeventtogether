from django.contrib import admin

from persons.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass