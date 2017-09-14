# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-14 14:48
from __future__ import unicode_literals

import common.mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserInfo', '0007_change_on_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassYearMailingListAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_year', models.IntegerField(default=2018)),
                ('access_type', models.CharField(choices=[('sub', 'Subscribe'), ('snd', 'Send')], default='snd', max_length=3)),
            ],
            bases=(common.mixins.ModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GroupMailingListAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.CharField(choices=[('sub', 'Subscribe'), ('snd', 'Send')], default='snd', max_length=3)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            bases=(common.mixins.ModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
                ('description', models.CharField(default='', max_length=128)),
            ],
            bases=(common.mixins.ModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MailingListSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MailingLists.MailingList')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(common.mixins.ModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PledgeClassMailingListAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.CharField(choices=[('sub', 'Subscribe'), ('snd', 'Send')], default='snd', max_length=3)),
                ('mailing_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MailingLists.MailingList')),
                ('pledge_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserInfo.PledgeClass')),
            ],
            bases=(common.mixins.ModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='groupmailinglistaccess',
            name='mailing_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MailingLists.MailingList'),
        ),
        migrations.AddField(
            model_name='classyearmailinglistaccess',
            name='mailing_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MailingLists.MailingList'),
        ),
        migrations.AlterUniqueTogether(
            name='pledgeclassmailinglistaccess',
            unique_together=set([('mailing_list', 'pledge_class', 'access_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='mailinglistsubscription',
            unique_together=set([('mailing_list', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupmailinglistaccess',
            unique_together=set([('mailing_list', 'group', 'access_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='classyearmailinglistaccess',
            unique_together=set([('mailing_list', 'class_year', 'access_type')]),
        ),
    ]
