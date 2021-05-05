from django.http import HttpResponseRedirect
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from events.views.events import ProfileEventDetailsView, DeleteEventView, EditEventView, ProfileRegisteredEventsView, \
    DesinscriptionEventView, ProfileFinishedEventsView, EventDetailsView, EventCreateView, EventInscriptionView, \
    EventDescriptionView, ProfileRatingFinishedEventsView, EventFavoriteView, UnfavoriteEventView, ProfileFavoriteEventsView
from events.views.persons import MyLoginView, InscriptionView, EditProfilView, DetailProfilView, HomeView, ProfilShowUserView, \
    ProfilShowEventView

urlpatterns = [
    path('', lambda r: HttpResponseRedirect(reverse_lazy('events')), name='accueil'),
    path('connexion', MyLoginView.as_view(), name='login'),
    path('deconnexion', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('inscription', InscriptionView.as_view(), name='inscription'),
    path('home', HomeView.as_view(), name='home'),
    path('evenements', EventDetailsView.as_view(), name='events'),
    path('evenements/creer', EventCreateView.as_view(), name='create-event'),
    path('evenement/description/<int:event_id>', EventDescriptionView.as_view(), name='description-event'),
    path('evenement/inscription/<int:event_id>', EventInscriptionView.as_view(), name='inscription-event'),
    path('evenement/favoris/<int:event_id>', EventFavoriteView.as_view(), name='favorite-event'),
    path('evenement/favoris/desinscription/<int:favorite_id>', UnfavoriteEventView.as_view(), name='unfavorite-event'),
    path('profil', DetailProfilView.as_view(), name='profil'),
    path('profil/modifier', EditProfilView.as_view(), name='profil-edit'),
    path('profil/evenements', ProfileEventDetailsView.as_view(), name='profil-events'),
    path('profil/evenements/inscrit', ProfileRegisteredEventsView.as_view(), name='profil-registered_events'),
    path('profil/evenements/finis', ProfileFinishedEventsView.as_view(), name='profil-finished-events'),
    path('profil/evenements/favoris', ProfileFavoriteEventsView.as_view(), name='profil-favorite-events'),
    path('profil/evenements/<int:event_id>', ProfileRatingFinishedEventsView.as_view(), name='profil-rating-finished-events'),
    path('profil/evenements/<int:inscription_id>/inscris/supprimer', DesinscriptionEventView.as_view(), name='desinscription-event'),
    path('profil/evenements/<int:event_id>/modifier', EditEventView.as_view(), name='edit-event'),
    path('profil/evenements/<int:event_id>/supprimer', DeleteEventView.as_view(), name='delete-event'),
    path('profil/utilisateur/<int:person_id>', ProfilShowUserView.as_view(), name='profil-show-user'),
    path('profil/utilisateur/<int:person_id>/evenement', ProfilShowEventView.as_view(), name='profil-show-events'),
    # path('recherche', SearchView.as_view(), name='search')
]