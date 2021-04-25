# Generated by Django 3.1.2 on 2021-04-17 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0005_auto_20210218_0929'),
        ('events', '0011_auto_20210218_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.person')),
            ],
        ),
    ]
