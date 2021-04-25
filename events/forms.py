from django import forms
from django.core.exceptions import ValidationError

from events.models import Event, Karma
from persons.models import Person
from users.models import User


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['person', 'created_at']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class KarmaForm(forms.ModelForm):
    class Meta:
        model = Karma
        exclude = ['person', 'event', ]
        widgets = {
            'note': forms.NumberInput(attrs={'max': 10, 'min': 0})
        }


class PersonForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Person
        exclude = ['user', 'created_at', 'karma']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'email@gmail.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '0612344321'}),
            'birth_date': forms.DateTimeInput(attrs={'type': 'date', })
        }


class ProfilForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = Person
        exclude = ['user', 'created_at', 'karma', 'person_type', 'birth_date', 'pseudo', ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '0612344321'}),

        }

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)
        if instance:
            self.fields['email'].initial = instance.user.email

    def clean_email(self):
        email = self.cleaned_data['email']
        person = self.instance
        qs = User.objects
        if person.pk:
            qs = qs.exclude(pk=person.user.id)
        is_used = qs.filter(email=email).exists()
        if is_used:
            raise ValidationError('Cette adresse email est déjà utilisée')

        return email
