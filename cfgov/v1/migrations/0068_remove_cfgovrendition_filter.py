# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0067_add_expandables_to_blog_pages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cfgovrendition',
            name='filter',
        ),
    ]
