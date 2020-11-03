from django.urls import path

from events.views import EventDetailsView, EventCreateView

urlpatterns = [
    path('details', EventDetailsView.as_view(), name='details'),
    path('creer', EventCreateView.as_view(), name='new-event'),
]