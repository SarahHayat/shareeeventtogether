from django.db import models

class Event(models.Model):

    PARTY_CATEGORY = 'party'
    GAME_CATEGORY = 'game'
    TOURISM_CATEGORY = 'tourism'
    AREA_CATEGORY = 'area'

    CATEGORY_CHOICES = (
        (PARTY_CATEGORY, 'soiree'),
        (GAME_CATEGORY, 'jeux'),
        (TOURISM_CATEGORY, 'tourisme'),
        (AREA_CATEGORY, 'plein air')
    )

    person = models.ForeignKey('persons.Person', on_delete=models.CASCADE, null=True)
    title = models.CharField('titre', max_length=150)
    description = models.TextField('description')
    address = models.CharField('adresse', max_length=100)
    zip_code = models.IntegerField('code postal')
    city = models.CharField('ville', max_length=50)
    category = models.CharField('categorie', choices=CATEGORY_CHOICES, max_length=20)
    created_at = models.DateTimeField('crée à', auto_now=True)
    event_date = models.DateTimeField('date evenement', auto_now=False)

    def __str__(self):
        return f'{self.title}-{self.category}'
