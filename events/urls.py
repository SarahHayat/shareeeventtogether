from django.urls import path

from events.views import EventDetailsView, EventCreateView, EventInscriptionView

urlpatterns = [
    path('details', EventDetailsView.as_view(), name='details'),
    path('creer', EventCreateView.as_view(), name='new-event'),
    path('<int:event_id>/inscription', EventInscriptionView.as_view(), name='inscription-event'),
]