# Generated by Django 2.0.6 on 2018-07-03 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_auto_20180630_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('trade_type', models.IntegerField()),
                ('price', models.FloatField()),
                ('amount', models.FloatField()),
                ('reservation_price', models.FloatField()),
                ('coin_id', models.IntegerField()),
                ('is_complete', models.BooleanField(default=False)),
                ('is_cancel', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Account')),
            ],
        ),
    ]
