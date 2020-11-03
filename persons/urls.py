from django.http import HttpResponseRedirect
from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views

from events.views import MyEventDetailsView, DeleteEventView, EditEventView
from persons.views import HomeView, InscriptionView, EditProfilView, DetailProfilView

urlpatterns = [
    path('', lambda r: HttpResponseRedirect(reverse_lazy('home')), name='accueil'),
    path('connexion', auth_views.LoginView.as_view(template_name="persons/registration/login.html"),name='login'),
    path('deconnexion', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('inscription', InscriptionView.as_view(), name='inscription'),
    path('home', HomeView.as_view(), name='home'),
    path('profil', DetailProfilView.as_view(), name='profil'),
    path('profil/edit', EditProfilView.as_view(), name='profil-edit'),
    path('profil/events', MyEventDetailsView.as_view(), name='profil-events'),
    path('profil/events/<int:event_id>/delete', DeleteEventView.as_view(), name='delete-event'),
    path('profil/events/<int:event_id>/modifier', EditEventView.as_view(), name='edit-event'),
    path('event/', include('events.urls'))


]
