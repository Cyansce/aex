# Generated by Django 2.0.6 on 2018-06-28 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20180628_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('api_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
