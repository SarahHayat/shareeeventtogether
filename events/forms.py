from django import forms

from events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['person', 'created_at']
        widgets = {
            'event_date': forms.DateInput(attrs={'class':'datepicker'}),
        }
