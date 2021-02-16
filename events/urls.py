from django.http import HttpResponseRedirect
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from events.views.events import ProfileEventDetailsView, DeleteEventView, EditEventView, ProfileRegisteredEventsView, \
    DesinscriptionEventView, ProfileFinishedEventsView, EventDetailsView, EventCreateView, EventInscriptionView, \
    EventDescriptionView, ProfileRatingFinishedEventsView, SearchView
from events.views.persons import InscriptionView, EditProfilView, DetailProfilView, HomeView

urlpatterns = [
    path('', lambda r: HttpResponseRedirect(reverse_lazy('events')), name='accueil'),
    path('connexion', auth_views.LoginView.as_view(template_name="persons/registration/login.html"), name='login'),
    path('deconnexion', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('inscription', InscriptionView.as_view(), name='inscription'),
    path('home', HomeView.as_view(), name='home'),
    path('evenements', EventDetailsView.as_view(), name='events'),
    path('evenements/creer', EventCreateView.as_view(), name='create-event'),
    path('evenement/description/<int:event_id>', EventDescriptionView.as_view(), name='description-event'),
    path('evenement/inscription/<int:event_id>', EventInscriptionView.as_view(), name='inscription-event'),
    path('profile', DetailProfilView.as_view(), name='profil'),
    path('profile/modifier', EditProfilView.as_view(), name='profil-edit'),
    path('profile/evenements', ProfileEventDetailsView.as_view(), name='profil-events'),
    path('profile/evenements/inscrit', ProfileRegisteredEventsView.as_view(), name='profil-registered_events'),
    path('profile/evenements/finis', ProfileFinishedEventsView.as_view(), name='profil-finished-events'),
    path('profile/evenements/<int:event_id>', ProfileRatingFinishedEventsView.as_view(), name='profil-rating-finished-events'),
    path('profile/evenements/<int:inscription_id>/inscris/supprimer', DesinscriptionEventView.as_view(), name='desinscription-event'),
    path('profile/evenements/<int:event_id>/modifier', EditEventView.as_view(), name='edit-event'),
    path('profile/evenements/<int:event_id>/supprimer', DeleteEventView.as_view(), name='delete-event'),
    path('recherche', SearchView.as_view(), name='search')
]