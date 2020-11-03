from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View

from persons import navigation
from persons.forms import PersonForm, ProfilForm
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
            return redirect(reverse('home'))
        else:
            return redirect(reverse('login'))


class DetailProfilView(PersonView):
    def get(self, request):
        user = request.user
        person = Person.objects.get(user=user)
        form = ProfilForm(instance=person)
        context = {
            'person': person,
            'form': form,
            'navigation_items': navigation.navigation_items(navigation.NAV_HOME),
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
            'navigation_items': navigation.navigation_items(navigation.NAV_HOME),
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
                'navigation_items': navigation.navigation_items(navigation.NAV_HOME),

            }
            return render(request, 'persons/profil/profil_edit.html', context)
