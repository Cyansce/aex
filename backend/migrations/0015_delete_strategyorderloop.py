# Generated by Django 2.0.6 on 2018-06-28 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_delete_tradeconfig'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StrategyOrderLoop',
        ),
    ]