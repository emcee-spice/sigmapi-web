# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-11 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('PartyList', '0016_auto_20180411_1734'), ('PartyList', '0017_auto_20180411_1739'), ('PartyList', '0018_auto_20180411_1740')]

    dependencies = [
        ('PartyList', '0015_add_count_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partyguest',
            name='timeFirstSignedIn',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='partyguest',
            name='timeFirstSignedIn',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='partyguest',
            name='timeFirstSignedIn',
            field=models.DateTimeField(null=True),
        ),
    ]