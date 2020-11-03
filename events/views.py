from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View

from events.forms import EventForm
from events.models import Event
from persons import navigation
from persons.models import Person
from persons.views import PersonView


class EventDetailsView(View):
    def get(self, request):
        events = Event.objects.all()
        user = request.user
        context = {
            'user': user,
            'events': events,
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
        print("error : " + str(form.errors))
        print("error : " + str(form))

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
