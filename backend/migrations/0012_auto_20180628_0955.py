# Generated by Django 2.0.6 on 2018-06-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20180628_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='StrategyOrderLoop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField()),
                ('amount', models.FloatField()),
                ('timeout', models.IntegerField()),
                ('cancel_count', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='orderlog',
            name='is_strategy_complete',
            field=models.BooleanField(default=False),
        ),
    ]
