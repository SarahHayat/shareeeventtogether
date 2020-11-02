from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class PersonView(LoginRequiredMixin, View):
    login_url = 'login'


class HomeView(PersonView):
    def get(self, request):
        text = "hello"
        context = {
            'text': text,
        }
        return render(request, 'persons/home.html', context)