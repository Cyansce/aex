# Generated by Django 2.0.6 on 2018-06-28 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_strategyorderloop'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategyorderloop',
            name='is_api',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]