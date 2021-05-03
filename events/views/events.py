import requests
from django.core import serializers
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views import View
from django.db.models import Q

import json

from events.forms import EventForm, KarmaForm
from events.models import InscriptionEvent, Event, Karma, FavoriteEvent
from events.models_helpers import get_person_by_user, get_all_events, get_events_by_user, get_event_by_id, \
    get_if_person_is_registered, get_inscription_event_person, get_inscription_by_id, ALL_CATEGORIES, \
    get_filtered_events, get_events_categories, get_person_by_id, get_if_event_is_fav, get_favorite_by_id, \
    get_favorite_event_person

from events import navigation
from events.views.persons import PersonView


class EventDetailsView(View):
    def get(self, request):
        user = request.user
        # if user.pk:
        query = self.request.GET.get('q')
        person = get_person_by_user(user) if user.pk else None
        api_request = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={person.address}&postcode={person.zip_code}&city={person.city}&autocomplete=0&limit=1") if user.pk else None
        reponse = api_request.json() if user.pk else None
        coordonate_x = reponse['features'][0]['geometry']['coordinates'][1] if user.pk else 48.8
        coordonate_y = reponse['features'][0]['geometry']['coordinates'][0] if user.pk else 2.3
        category_filter = request.GET.get('category_filter', ALL_CATEGORIES)
        lieu_filter = request.GET.get('lieu')

        if query is not None:
            events_search = Event.objects.filter(Q(title__icontains=query) | Q(category__icontains=query)).filter(
                event_date__gte=timezone.now())
            filtered_events = get_filtered_events(events_search, category_filter, lieu_filter)
            category = get_events_categories(events_search)
        elif lieu_filter is not None:
            events = Event.objects.filter(city=lieu_filter, event_date__gte=timezone.now())
            filtered_events = get_filtered_events(events, category_filter, lieu_filter)
            category = get_events_categories(events)
            api_request = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={lieu_filter}&autocomplete=0&limit=1")
            reponse = api_request.json()
            coordonate_x = reponse['features'][0]['geometry']['coordinates'][1]
            coordonate_y = reponse['features'][0]['geometry']['coordinates'][0]
        else:
            events = get_all_events()
            filtered_events = get_filtered_events(events, category_filter, lieu_filter)
            category = get_events_categories(events)
        order_filter = request.GET.get('order_filter', 'event_date')
        if order_filter == 'event_date':
            filtered_events = filtered_events.order_by('event_date')
        else:
            filtered_events = filtered_events.order_by('-event_date')

        context = {
            'user': user,
            'person': person,
            'filtered_events': filtered_events,
            'category': category,
            'lieu_filter': lieu_filter,
            'order_filter': order_filter,
            'category_filter': category_filter,
            'query': query,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
            'coordonate_x': str(coordonate_x).replace(",", "."),
            'coordonate_y': str(coordonate_y).replace(",", ".")
        }
        return render(request, 'events/event_list.html', context)


class EventCreateView(PersonView):
    def get(self, request):
        user = request.user
        person = get_person_by_user(user)
        form = EventForm()
        context = {
            'user': user,
            'person': person,
            'form': form,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
        }
        return render(request, 'events/event_new.html', context)

    def post(self, request):
        user = request.user
        person = get_person_by_user(user)
        form = EventForm(request.POST)
        print(form.errors)
        if form.is_valid():
            event = form.save(commit=False)
            event.person = person
            event.created_at = datetime.now()

            event.save()
            return redirect(reverse('events'))
        else:
            form = EventForm()
            context = {
                'user': user,
                'person': person,
                'form': form,
                'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
            }
            return render(request, 'events/event_new.html', context)


class ProfileEventDetailsView(PersonView):
    def get(self, request):
        user = request.user
        events = get_events_by_user(user)
        person = get_person_by_user(user)
        context = {
            'user': user,
            'events': events,
            'person': person,
            'navigation_items': navigation.navigation_items(navigation.NAV_PROFIL),
        }
        return render(request, 'persons/events/my_events_details.html', context)


class ProfileRegisteredEventsView(PersonView):
    def get(self, request):
        user = request.user
        person = get_person_by_user(user)
        today = datetime.now()
        inscription_events = get_inscription_event_person(person).filter(event__event_date__gt=today)
        context = {
            'user': user,
            'person': person,
            'inscription_events': inscription_events,
            'navigation_items': navigation.navigation_items(navigation.NAV_PROFIL),
        }
        return render(request, 'persons/events/my_registered_events.html', context)


class ProfileFinishedEventsView(PersonView):
    def get(self, request):
        user = request.user
        person = get_person_by_user(user)
        today = datetime.now()
        inscription_events = get_inscription_event_person(person).filter(event__event_date__lt=today)
        form = KarmaForm()

        context = {
            'user': user,
            'person': person,
            'form': form,
            'inscription_events': inscription_events,
            'navigation_items': navigation.navigation_items(navigation.NAV_PROFIL),
        }
        return render(request, 'persons/events/my_finished_events.html', context)


class ProfileRatingFinishedEventsView(PersonView):

    def post(self, request, event_id, *args, **kwargs):
        try:
            user = request.user
            person = get_person_by_user(user)
            event = get_event_by_id(event_id)
            person_event = get_person_by_id(event.person.pk)
            form = KarmaForm(data=request.POST)
            if form.is_valid():
                karma = form.save(commit=False)
                karma.event = event
                karma.person = person
                karma.save()
                note = Karma.objects.filter(event__person=event.person).aggregate(Avg('note'))
                person_event.note = note['note__avg']
                person_event.save()
                return redirect(reverse('profil-finished-events'))
            else:
                return redirect(reverse('events'))
        except Event.DoesNotExist:
            raise Http404()


class DesinscriptionEventView(PersonView):
    def get(self, request, inscription_id):
        inscription = get_inscription_by_id(inscription_id)
        inscription.delete()
        return redirect(request.META.get('HTTP_REFERER'))


class DeleteEventView(PersonView):
    def get(self, request, event_id):
        event = get_event_by_id(event_id)
        event.delete()
        return redirect(reverse('profil-events'))


class EditEventView(PersonView):
    def get(self, request, event_id):
        user = request.user
        person = get_person_by_user(user)
        event = get_event_by_id(event_id)
        form = EventForm(instance=event)
        context = {
            'person': person,
            'form': form,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
        }
        return render(request, 'persons/events/my_events_form.html', context)

    def post(self, request, event_id):
        user = request.user
        person = get_person_by_user(user)
        event = get_event_by_id(event_id)
        form = EventForm(instance=event, data=request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.person = person
            event.created_at = datetime.now()
            event.save()
            return redirect(reverse('profil-events'))
        else:
            form = EventForm(instance=event)
            context = {
                'person': person,
                'form': form,
                'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),

            }
            return render(request, 'persons/events/my_events_form.html', context)


class EventDescriptionView(View):
    def get(self, request, event_id):
        user = request.user
        event = get_event_by_id(event_id)
        person = get_person_by_user(user) if user.pk else None
        is_registered = get_if_person_is_registered(person, event)
        is_favorite = get_if_event_is_fav(person, event)
        favorite = None
        inscrit = None
        if is_favorite:
            favorite = FavoriteEvent.objects.get(person=person, event=event) if user.pk else None
        if is_registered:
            inscrit = InscriptionEvent.objects.get(person=person, event=event) if user.pk else None

        events_caroussel = Event.objects.filter(category=event.category, event_date__gte=timezone.now()).exclude(pk=event_id)
        context = {
            'user': user,
            'person': person,
            'event': event,
            'is_registered': is_registered,
            'is_favorite': is_favorite,
            'favorite': favorite,
            'inscrit': inscrit,
            'events_caroussel' : events_caroussel,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
        }
        return render(request, 'events/event_detail.html', context)


class EventInscriptionView(PersonView):
    def get(self, request, event_id, *args, **kwargs):
        user = request.user
        person = get_person_by_user(user)
        event = get_event_by_id(event_id)
        is_registered = get_if_person_is_registered(person, event)
        if not is_registered or person != event.person:
            inscription = InscriptionEvent(person=person, event=event)
            inscription.save()
        return redirect(reverse('description-event', kwargs={'event_id': event.pk}))



class EventFavoriteView(PersonView):
    def get(self, request, event_id, *args, **kwargs):
        user = request.user
        person = get_person_by_user(user)
        event = get_event_by_id(event_id)
        favorite = FavoriteEvent(person=person, event=event)
        favorite.save()
        return redirect(reverse('description-event', kwargs={'event_id': event.pk}))


class UnfavoriteEventView(PersonView):
    def get(self, request, favorite_id):
        favorite = get_favorite_by_id(favorite_id)
        favorite.delete()
        return redirect(request.META.get('HTTP_REFERER'))


class ProfileFavoriteEventsView(PersonView):
    def get(self, request):
        user = request.user
        person = get_person_by_user(user)
        today = datetime.now()
        favorite_events = get_favorite_event_person(person).filter(event__event_date__gt=today)
        context = {
            'user': user,
            'person': person,
            'favorite_events': favorite_events,
            'navigation_items': navigation.navigation_items(navigation.NAV_PROFIL),

        }
        return render(request, 'persons/events/my_favorite_events.html', context)
