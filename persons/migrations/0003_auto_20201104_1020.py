# Generated by Django 3.1.2 on 2020-11-04 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20201102_0936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='karma',
            new_name='note',
        ),
    ]
