# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20140915_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='html',
            name='url',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
