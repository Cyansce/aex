# Generated by Django 2.0.6 on 2018-06-26 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_apiaccount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apiaccount',
            old_name='secret_key',
            new_name='skey',
        ),
    ]