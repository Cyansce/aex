# Generated by Django 2.0.6 on 2018-07-06 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_apiconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationorder',
            name='reservation_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
