from django.contrib import admin

from events.models import Karma
from persons.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(Karma)
class KarmaAdmin(admin.ModelAdmin):
    pass