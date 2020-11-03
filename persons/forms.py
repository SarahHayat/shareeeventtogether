from django import forms

from persons.models import Person


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
            'birth_date': forms.DateTimeInput(attrs={
                'type': 'date',
            })
        }
