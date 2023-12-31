# Generated by Django 4.2.5 on 2023-10-02 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('starting_bid', models.IntegerField(default=0)),
                ('highest_bidder', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='YourModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('image', models.URLField(default=None)),
                ('category', models.CharField(default=None, max_length=64)),
                ('description', models.TextField(default=None)),
                ('closed', models.BooleanField(default=False)),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.bids')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('yourmodel', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auctions.yourmodel')),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(default=None, max_length=255)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('yourmodel', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auctions.yourmodel')),
            ],
        ),
        migrations.CreateModel(
            name='auctionswon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('image', models.URLField()),
                ('category', models.CharField(default=None, max_length=64)),
                ('description', models.TextField(default=None)),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.bids')),
            ],
        ),
    ]
