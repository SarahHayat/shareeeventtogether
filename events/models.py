from django.db import models


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

    def getEventId(self):
        return self.pk

    def __str__(self):
        return f'{self.title}-{self.category}'


class InscriptionEvent(models.Model):
    person = models.ForeignKey('persons.Person', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    def getKarma(self):
        print("HELLO")
        print(f' KARMA {Karma.objects.get(person=self.person, event=self.event)}')
        return Karma.objects.get(person=self.person, event=self.event).note

    def __str__(self):
        return f'{self.person.pseudo} - {self.event.title}'


class Karma(models.Model):
    person = models.ForeignKey('persons.Person', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    note = models.IntegerField('Note', default=0)

    def __str__(self):
        return f'{self.person}-{self.event}-{self.note}'
