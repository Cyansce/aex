# Generated by Django 2.0.6 on 2018-06-27 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_coin_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_api', models.BooleanField()),
                ('account_name', models.CharField(max_length=50)),
                ('coin_name', models.CharField(max_length=20)),
                ('zone_name', models.CharField(max_length=20)),
                ('trade_type', models.IntegerField()),
                ('number', models.CharField(max_length=20)),
                ('price', models.FloatField(null=True)),
                ('amount', models.FloatField(null=True)),
                ('complete', models.BooleanField(verbose_name=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('relate_trade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='backend.OrderLog')),
            ],
        ),
    ]
