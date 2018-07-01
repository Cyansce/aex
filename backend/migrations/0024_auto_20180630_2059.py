# Generated by Django 2.0.6 on 2018-06-30 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_auto_20180630_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='strategyorderloop',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='strategyorderloop',
            name='is_api',
        ),
        migrations.AddField(
            model_name='strategyorderloop',
            name='account',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='backend.Account'),
            preserve_default=False,
        ),
    ]