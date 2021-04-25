from django.utils import timezone

from events.models import Event, InscriptionEvent, FavoriteEvent
from persons.models import Person

ALL_CATEGORIES = 'all'


def get_person_by_user(user):
    return Person.objects.get(user=user)


def get_all_events():
    return Event.objects.all().filter(event_date__gte=timezone.now())


def get_events_by_user(user):
    return Event.objects.filter(person__user=user)


def get_person_by_id(person_id):
    return Person.objects.get(pk=person_id)


def get_event_by_id(event_id):
    return Event.objects.get(pk=event_id)


def get_if_person_is_registered(person, event):
    return InscriptionEvent.objects.filter(person=person, event=event).exists()


def get_filtered_events(events, category_filter=ALL_CATEGORIES, lieu_filter=None):
    if category_filter != ALL_CATEGORIES:
        events = events.filter(category=category_filter)
    if lieu_filter is not None:
        events = events.filter(city=lieu_filter)
    return events


def get_events_categories(events):
    categories = list()
    categories.append((ALL_CATEGORIES, 'Tous', events.count()))
    for cat in Event.CATEGORY_CHOICES:
        categories.append((cat[0], cat[1], events.filter(category=cat[0]).count()))

    return categories


def get_inscription_event_person(person):
    return InscriptionEvent.objects.filter(person=person)


def get_inscription_by_id(inscription_id):
    return InscriptionEvent.objects.get(pk=inscription_id)


def get_if_event_is_fav(person, event):
    return FavoriteEvent.objects.filter(person=person, event=event).exists()

def get_favorite_by_id(favorite_id):
    return FavoriteEvent.objects.get(pk=favorite_id)

def get_favorite_event_person(person):
    return FavoriteEvent.objects.filter(person=person)
