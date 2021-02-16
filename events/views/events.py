from django.db.models import Avg
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View
from django.db.models import Q

from events.forms import EventForm, KarmaForm
from events.models import InscriptionEvent, Event, Karma
from events.models_helpers import get_person_by_user, get_all_events, get_events_by_user, get_event_by_id, \
    get_if_person_is_registered, get_inscription_event_person, get_inscription_by_id, ALL_CATEGORIES, \
    get_filtered_events, get_events_categories, get_person_by_id

from events import navigation
from events.views.persons import PersonView


class EventDetailsView(View):
    def get(self, request):
        user = request.user
        if user.pk:
            person = get_person_by_user(user)
            category_filter = request.GET.get('category_filter', ALL_CATEGORIES)
            events = get_all_events()
            filtered_events = get_filtered_events(events, category_filter)
            order_filter = request.GET.get('order_filter', 'event_date')
            if order_filter == 'event_date':
                filtered_events = filtered_events.order_by('event_date')
            else:
                filtered_events = filtered_events.order_by('-event_date')
            context = {
                'user': user,
                'person': person,
                'filtered_events': filtered_events,
                'category': get_events_categories(events),
                'order_filter': order_filter,
                'category_filter': category_filter,
                'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),

            }
        else:
            events = get_all_events()
            user = request.user
            context = {
                'user': user,
                'events': events,
                'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),

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
        user = request.user
        context = {
            'user': user,
            'events': events,
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
            # person = get_person_by_id(person_id)
            event = get_event_by_id(event_id)
            form = KarmaForm(data=request.POST)
            if form.is_valid():
                karma = form.save(commit=False)
                karma.event = event
                karma.person = person
                karma.save()

                # moyenne = Karma.objects.all().aggregate(Avg('note'))
                # print('moyenne')
                # print(moyenne)
                # person.note = moyenne
                person.save()
                return redirect(reverse('profil-finished-events'))
            else:
                return redirect(reverse('events'))
        except Event.DoesNotExist:
            raise Http404()


class DesinscriptionEventView(PersonView):
    def get(self, request, inscription_id):
        inscription = get_inscription_by_id(inscription_id)
        inscription.delete()
        return redirect(reverse('profil-registered_events'))


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
        print(event.event_date)
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


class EventDescriptionView(PersonView):
    def get(self, request, event_id):
        user = request.user
        person = get_person_by_user(user)
        event = get_event_by_id(event_id)
        is_registered = get_if_person_is_registered(person, event)
        context = {
            'user': user,
            'person': person,
            'event': event,
            'is_registered': is_registered,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
        }
        return render(request, 'events/event_detail.html', context)


class EventInscriptionView(PersonView):
    def get(self, request, event_id, **kwargs):
        user = request.user
        person = get_person_by_user(user)
        event = get_event_by_id(event_id)
        inscription = InscriptionEvent(person=person, event=event)
        inscription.save()
        return redirect(reverse('description-event', kwargs={'event_id': event.pk}))

class SearchView(PersonView):
    def get(self, request):
        query = self.request.GET.get('q')
        events = Event.objects.filter( Q(title__unaccent__icontains=query) | Q(category__unaccent__icontains=query))
        user = request.user
        person = get_person_by_user(user)
        context = {
            'user': user,
            'person': person,
            'events': events,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
        }
        return render(request, 'events/event_search.html', context)