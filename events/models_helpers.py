from events.models import Event, InscriptionEvent
from persons.models import Person


def get_person_by_user(user):
    return Person.objects.get(user=user)


def get_all_events():
    return Event.objects.all()


def get_events_by_user(user):
    return Event.objects.filter(person__user=user)


def get_event_by_id(event_id):
    return Event.objects.get(pk=event_id)


def get_if_person_is_registered(person, event):
    return InscriptionEvent.objects.filter(person=person, event=event).exists()


def get_inscription_event_person(person):
    return InscriptionEvent.objects.filter(person=person)