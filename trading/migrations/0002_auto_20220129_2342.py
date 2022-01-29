# Generated by Django 2.2.6 on 2022-01-29 18:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='global',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='UserShareTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidShares', models.IntegerField(default=0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Company')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidShares', models.IntegerField(default=0)),
                ('bidPrice', models.IntegerField(default=0)),
                ('buySell', models.BooleanField(default=1)),
                ('transactionTime', models.DateTimeField(default=datetime.datetime.now)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Company')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='SellTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidPrice', models.IntegerField(default=0)),
                ('bidShares', models.IntegerField(default=0)),
                ('transactionTime', models.DateTimeField(default=datetime.datetime.now)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Company')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='BuyTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidPrice', models.IntegerField(default=0)),
                ('bidShares', models.IntegerField(default=0)),
                ('transactionTime', models.DateTimeField(default=datetime.datetime.now)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Company')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Profile')),
            ],
        ),
    ]
