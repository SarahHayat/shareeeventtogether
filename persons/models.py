from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    TYPE_PARTICULIER = 'particulier'
    TYPE_PROFESSIONNEL = 'professionnel'

    TYPE_CHOICES = (
        (TYPE_PARTICULIER, 'particulier'),
        (TYPE_PROFESSIONNEL, 'professionnel')
    )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    first_name = models.CharField('prenom', max_length=100)
    last_name = models.CharField('nom', max_length=100)
    birth_date = models.DateField('date naissance')
    address = models.CharField('adresse', max_length=250)
    zip_code = models.IntegerField('code postal')
    city = models.CharField('ville', max_length=50)
    country = models.CharField('pays', max_length=100)
    phone_number = PhoneNumberField('telephone')
    pseudo = models.CharField('pseudo', max_length=50)
    person_type = models.CharField('type', choices=TYPE_CHOICES, max_length=15)
    created_at = models.DateTimeField('crée à', auto_now=True)
    note = models.IntegerField('karma', null=True, blank=True)
    imageProfil = models.FileField('image', null=True, default='utilisateur-de-profil.svg')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
