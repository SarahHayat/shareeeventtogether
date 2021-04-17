from django.contrib import admin

from events.models import Event, InscriptionEvent, Karma, FavoriteEvent

from persons.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Karma)
class KarmaAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(InscriptionEvent)
class InscriptionEventAdmin(admin.ModelAdmin):
    pass


@admin.register(FavoriteEvent)
class FavoriteEventAdmin(admin.ModelAdmin):
    pass
