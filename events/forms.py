from django import forms

from events.models import Event, Karma


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['person', 'created_at']

        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local', })
        }


class KarmaForm(forms.ModelForm):
    class Meta:
        model = Karma
        fields = ('note',)
        widgets = {
            'note': forms.NumberInput(attrs={'max': 10, 'min': 0 })
        }
