from django.db import models
import requests


class Event(models.Model):
    PARTY_CATEGORY = 'soiree'
    GAME_CATEGORY = 'jeux'
    TOURISM_CATEGORY = 'tourisme'
    AREA_CATEGORY = 'plein air'

    CATEGORY_CHOICES = (
        (PARTY_CATEGORY, 'soiree'),
        (GAME_CATEGORY, 'jeux'),
        (TOURISM_CATEGORY, 'tourisme'),
        (AREA_CATEGORY, 'plein air')
    )

    person = models.ForeignKey('persons.Person', on_delete=models.CASCADE)
    title = models.CharField('titre', max_length=150)
    description = models.TextField('description')
    address = models.CharField('adresse', max_length=100)
    zip_code = models.IntegerField('code postal')
    city = models.CharField('ville', max_length=50)
    category = models.CharField('categorie', choices=CATEGORY_CHOICES, max_length=20)
    created_at = models.DateTimeField('crée à', auto_now=True)
    event_date = models.DateTimeField('date evenement', auto_now=False)
    coordonate_x = models.CharField('coordonnée X',max_length=10 ,null=True, blank=True)
    coordonate_y = models.CharField('coordonnée Y',max_length=10 , null=True, blank=True)

    def save(self, *args, **kwargs):

        api_request = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={self.address}&postcode={self.zip_code}&city={self.city}&autocomplete=0&limit=1")
        reponse = api_request.json()

        coordonate_x = reponse['features'][0]['geometry']['coordinates'][1]
        coordonate_y = reponse['features'][0]['geometry']['coordinates'][0]

        self.address = reponse['features'][0]['properties']['name']
        self.zip_code = reponse['features'][0]['properties']['postcode']
        self.city = reponse['features'][0]['properties']['city'].upper()
        self.coordonate_x = str(coordonate_x).replace(",", ".")
        self.coordonate_y = str(coordonate_y).replace(",", ".")
        super().save(*args, **kwargs)

    def getEventId(self):
        return self.pk

    def __str__(self):
        return f'{self.title}-{self.category}'


class InscriptionEvent(models.Model):
    person = models.ForeignKey('persons.Person', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    def getKarma(self):
        return Karma.objects.get(person=self.person, event=self.event).note

    def __str__(self):
        return f'{self.person.pseudo} - {self.event.title}'


class Karma(models.Model):
    person = models.ForeignKey('persons.Person', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    note = models.IntegerField('Note', default=0)


    def __str__(self):
        return f'{self.person}-{self.event}-{self.note}'


class FavoriteEvent(models.Model):
    person = models.ForeignKey('persons.Person', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.person.pseudo} a mit en fav {self.event.title}'