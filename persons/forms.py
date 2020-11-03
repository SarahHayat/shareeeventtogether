from django import forms
from django.core.exceptions import ValidationError

from persons.models import Person
from users.models import User


class PersonForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Password', max_length=250)

    class Meta:
        model = Person
        exclude = ['user', 'created_at', 'karma']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'email@gmail.com'}),
            'password': forms.PasswordInput(attrs={'placeholder': '*****'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '0612344321'}),
            'birth_date': forms.DateTimeInput(attrs={'type': 'date',})
        }


class ProfilForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = Person
        exclude = ['user', 'created_at', 'karma', 'person_type', 'birth_date', 'pseudo',]
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
