# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_investors_data'),
        ('funds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startdate', models.DateTimeField(auto_now_add=True)),
                ('enddate', models.DateTimeField(null=True, blank=True)),
                ('fundaccount', models.ForeignKey(to='funds.FundAccount')),
                ('transaction', models.ForeignKey(to='app.Transaction')),
            ],
        ),
    ]
