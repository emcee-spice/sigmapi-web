# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PartyList', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklistedguest',
            name='details',
            field=models.TextField(),
        ),
    ]
