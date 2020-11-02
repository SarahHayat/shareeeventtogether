# Generated by Django 3.1.2 on 2020-11-02 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='titre')),
                ('description', models.TextField(verbose_name='description')),
                ('address', models.CharField(max_length=100, verbose_name='adresse')),
                ('zip_code', models.IntegerField(verbose_name='code postal')),
                ('city', models.CharField(max_length=50, verbose_name='ville')),
                ('category', models.CharField(choices=[('party', 'soiree'), ('game', 'jeux'), ('tourism', 'tourisme'), ('area', 'plein air')], max_length=20, verbose_name='categorie')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='crée à')),
                ('event_date', models.DateTimeField(verbose_name='date evenement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]