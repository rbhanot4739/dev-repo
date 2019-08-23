# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('job', models.CharField(max_length=20, blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, related_name='children', to='family.FamilyMember')),
            ],
        ),
    ]
