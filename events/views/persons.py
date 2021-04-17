from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views import View

from events import navigation
from events.forms import PersonForm, ProfilForm
from events.models import Event, InscriptionEvent
from events.models_helpers import get_person_by_id, get_if_person_is_registered
from persons.models import Person
from users.models import User


class PersonView(LoginRequiredMixin, View):
    login_url = 'login'


class HomeView(View):
    def get(self, request):
        user = request.user
        context = {
            'user': user,
            'navigation_items': navigation.navigation_items(navigation.NAV_HOME),
        }
        return render(request, 'persons/home.html', context)


class InscriptionView(View):
    def get(self, request):
        form = PersonForm()
        context = {
            'form': form,
        }
        return render(request, 'persons/registration/incription.html', context)

    def post(self, request):
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['password'])
            user.save()
            person.user = user
            person.created_at = datetime.now()
            person.save()
            return redirect(reverse('login'))
        else:
            context = {
                'form': form
            }
            return render(request, 'persons/registration/incription.html', context)


class DetailProfilView(PersonView):
    def get(self, request):
        user = request.user
        person = Person.objects.get(user=user)
        form = ProfilForm(instance=person)
        context = {
            'person': person,
            'form': form,
            'navigation_items': navigation.navigation_items(navigation.NAV_PROFIL),
        }
        return render(request, 'persons/profil/profil_detail.html', context)


class EditProfilView(PersonView):
    def get(self, request):
        user = request.user
        person = Person.objects.get(user=user)
        form = ProfilForm(instance=person)
        context = {
            'person': person,
            'form': form,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
        }
        return render(request, 'persons/profil/profil_edit.html', context)

    def post(self, request):
        user = request.user
        person = Person.objects.get(user=user)
        form = ProfilForm(instance=person, data=request.POST)
        if form.is_valid():
            person.user.email = form.cleaned_data['email']
            person.user.save()
            person.save()
            return redirect(reverse('profil'))
        else:
            form = ProfilForm(instance=person)
            context = {
                'person': person,
                'form': form,
                'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),

            }
            return render(request, 'persons/profil/profil_edit.html', context)


class ProfilShowUserView(PersonView):
    def get(self, request, person_id):
        person = get_person_by_id(person_id)
        user = request.user
        context = {
            'person': person,
            'user': user,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
        }

        return render(request, 'persons/profil/profil_show_user.html', context)


class ProfilShowEventView(PersonView):

    def get(self, request, person_id):
        person = get_person_by_id(person_id)
        user = request.user
        events = Event.objects.filter(person=person, event_date__gte=timezone.now())
        context = {
            'person': person,
            'user': user,
            'events': events,
            'navigation_items': navigation.navigation_items(navigation.NAV_EVENEMENT),
        }

        return render(request, 'persons/profil/profil_show_events.html', context)
