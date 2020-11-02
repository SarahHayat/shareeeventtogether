# Generated by Django 3.1.2 on 2020-11-02 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20201102_0936'),
        ('events', '0003_auto_20201102_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
        migrations.AddField(
            model_name='event',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='persons.person'),
        ),
    ]