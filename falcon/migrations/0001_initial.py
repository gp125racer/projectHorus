# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-24 04:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('uid', models.UUIDField(blank=True)),
                ('registered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(blank=True, default=1464065790.989082)),
                ('modified_at', models.DateTimeField(blank=True, default=1464065790.989105)),
                ('type', models.CharField(choices=[('100', 'Multi-Rotor'), ('200', 'Aircraft'), ('300', 'Ground')], max_length=100)),
                ('model', models.CharField(choices=[('100', 'Alpha'), ('200', 'Beta'), ('300', 'v1'), ('400', 'v2')], max_length=100)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FlightPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('uid', models.UUIDField(blank=True)),
                ('data', models.CharField(blank=True, max_length=2000)),
                ('created_at', models.DateTimeField(blank=True, default=1464065790.989799)),
                ('modified_at', models.DateTimeField(blank=True, default=1464065790.989823)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('uid', models.UUIDField(blank=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(blank=True, default=1464065790.990646)),
                ('modified_at', models.DateTimeField(blank=True, default=1464065790.990664)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='falcon.Device')),
                ('flight_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='falcon.FlightPlan')),
            ],
        ),
    ]