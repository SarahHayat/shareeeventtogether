from django.contrib import admin

from events.models import Event, InscriptionEvent


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(InscriptionEvent)
class InscriptionEventAdmin(admin.ModelAdmin):
    pass
