# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-18 13:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PartyListV2', '0013_partycountrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partyguest',
            name='_cached_json',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='partyguest',
            name='invite_used',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invites_used_for', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='partyguest',
            name='time_first_signed_in',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]