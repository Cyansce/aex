# Generated by Django 2.0.6 on 2018-06-27 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20180627_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlog',
            name='relate_trade',
        ),
    ]