# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 09:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('models3d', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='model3d',
            name='owner',
        ),
        migrations.AddField(
            model_name='model3d',
            name='model3d_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='model3d_owner', to=settings.AUTH_USER_MODEL, verbose_name='model3d_owner'),
            preserve_default=False,
        ),
    ]