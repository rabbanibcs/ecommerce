# Generated by Django 3.2.8 on 2021-11-12 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manageorder',
            name='payment',
        ),
    ]
