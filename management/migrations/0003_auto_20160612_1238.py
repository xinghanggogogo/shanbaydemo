# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 04:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_cet4_cet6_tofu_yasi'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='cet4',
            new_name='cet4word',
        ),
        migrations.RenameModel(
            old_name='cet6',
            new_name='cet6word',
        ),
        migrations.RenameModel(
            old_name='tofu',
            new_name='tofuword',
        ),
        migrations.RenameModel(
            old_name='yasi',
            new_name='yasiword',
        ),
    ]