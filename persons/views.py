from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View

from persons import navigation
from persons.forms import PersonForm
from users.models import User


class PersonView(LoginRequiredMixin, View):
    login_url = 'login'


class HomeView(View):
    def get(self, request):
        user= request.user
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
        print('form errors ' + str(form.errors))

        if form.is_valid():
            person = form.save(commit=False)
            print('avant user')
            user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['password'])
            print('user = ' + str(user))
            user.save()
            person.user = user
            person.created_at = datetime.now()
            print('person = '+ str(person))
            person.save()
            return redirect(reverse('home'))
        else:
            return redirect(reverse('login'))
