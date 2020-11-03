from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View

from events.forms import EventForm
from events.models import Event, InscriptionEvent
from persons import navigation
from persons.models import Person
from persons.views import PersonView


class EventDetailsView(View):
    def get(self, request):
        events = Event.objects.all()
        user = request.user
        person = Person.objects.get(user=user)
        is_inscrit = InscriptionEvent.objects.filter(person__pk__exact=person.pk).exists()
        context = {
            'user': user,
            'person': person,
            'events': events,
            'is_inscrit': is_inscrit,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),

        }
        return render(request, 'events/event_details.html', context)


class EventCreateView(PersonView):
    def get(self, request):
        user = request.user
        person = Person.objects.get(user=user)
        form = EventForm()
        context = {
            'user': user,
            'person': person,
            'form': form,
        }
        return render(request, 'events/event_new.html', context)

    def post(self, request):
        user = request.user
        person = Person.objects.get(user=user)
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.person = person
            event.created_at = datetime.now()
            event.save()
            return redirect(reverse('details'))
        else:
            form = EventForm()
            context = {
                'form': form
            }
            return render(request, 'events/event_new.html', context)


class MyEventDetailsView(PersonView):
    def get(self, request):
        user = request.user
        events = Event.objects.filter(person__user=user)
        user = request.user
        context = {
            'user': user,
            'events': events,
            'navigation_items': navigation.navigation_items(navigation.NAV_HOME),

        }
        return render(request, 'persons/events/my_events_details.html', context)


class DeleteEventView(PersonView):
    def get(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        event.delete()
        return redirect(reverse('profil-events'))


class EditEventView(PersonView):
    def get(self, request, event_id):
        user = request.user
        person = Person.objects.get(user=user)
        event = Event.objects.get(pk=event_id)
        form = EventForm(instance=event)
        context = {
            'person': person,
            'form': form,
            'navigation_items': navigation.navigation_items(navigation.NAV_HOME),
        }
        return render(request, 'persons/events/my_events_form.html', context)

    def post(self, request, event_id):
        user = request.user
        person = Person.objects.get(user=user)
        event = Event.objects.get(pk=event_id)
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
                'navigation_items': navigation.navigation_items(navigation.NAV_HOME),

            }
            return render(request, 'persons/events/my_events_form.html', context)


class EventInscriptionView(PersonView):
    def get(self, request, event_id):
        user = request.user
        person = Person.objects.get(user=user)
        event = Event.objects.get(pk=event_id)
        inscription = InscriptionEvent(person=person, event=event)
        inscription.save()
        return redirect(reverse('details'))
