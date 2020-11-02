from django.http import HttpResponseRedirect
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from persons.views import HomeView

urlpatterns = [
    path('', lambda r: HttpResponseRedirect(reverse_lazy('home')), name='accueil'),
    path('connexion', auth_views.LoginView.as_view(template_name="persons/registration/login.html"),name='login'),
    path('deconnexion', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home', HomeView.as_view(), name='home')

]
