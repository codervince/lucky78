# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from decimal import Decimal
from systems.models import System


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FundAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fundname', models.CharField(max_length=250)),
                ('description', models.TextField(help_text='logical reasoning', blank=True)),
                ('bettingratio', models.DecimalField(max_digits=6, decimal_places=2, blank=True)),
                ('managementfee', models.DecimalField(help_text='weekly fund/site management fee %', max_digits=6, decimal_places=2, blank=True)),
                ('performancefee', models.DecimalField(help_text='fee should performance exceed target %', max_digits=6, decimal_places=2, blank=True)),
                ('bailoutfee', models.DecimalField(help_text='fee if wishing to withdraw full capital within season (end of month) %', max_digits=6, decimal_places=2, blank=True)),
                ('currency', models.CharField(blank=True, help_text='fund base currency', max_length=10, choices=[(b'AUD', b'AUD'), (b'GBP', b'GBP')])),
                ('stakescap', models.DecimalField(max_digits=6, decimal_places=2, blank=True)),
                ('performancethreshold', models.DecimalField(max_digits=6, decimal_places=2, blank=True)),
                # ('systems', django.contrib.postgres.fields.ArrayField(null=True, base_field=models.CharField(max_length=50), size=None)),
                ('paysDividends', models.BooleanField()),
                ('bfbalance', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=2, blank=True)),
                ('winspbalance', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=2, blank=True)),
                ('openingbank', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=2, blank=True)),
                ('nosystems', models.SmallIntegerField(default=0, blank=True)),
                ('jratio', models.FloatField(default=None, blank=True)),
                ('oratio', models.FloatField(default=None, blank=True)),
                ('sratio', models.FloatField(default=None, blank=True)),
                ('tratio', models.FloatField(default=None, blank=True)),
                ('miratio', models.FloatField(default=None, blank=True)),
                ('betamounts', models.TextField(null=True, blank=True)),
                ('bfprices', models.TextField(null=True, blank=True)),
                ('dailybalances', models.TextField(null=True, blank=True)),
                ('systems', models.ManyToManyField(to='systems.System')),
                # ('betamounts', django.contrib.postgres.fields.ArrayField(null=True, base_field=models.DecimalField(max_digits=6, decimal_places=2), size=None)),
                # ('bfprices', django.contrib.postgres.fields.ArrayField(null=True, base_field=models.DecimalField(max_digits=6, decimal_places=2), size=None)),
                # ('dailybalances', django.contrib.postgres.fields.ArrayField(null=True, base_field=models.DecimalField(max_digits=6, decimal_places=2), size=None)),
                ('winpattern', models.TextField(null=True, blank=True)),
                ('placepattern', models.TextField(null=True, blank=True)),
                ('cashoutthreshold', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('totalinvested', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('startdate', models.DateTimeField(auto_now_add=True, null=True)),
                ('enddate', models.DateTimeField(auto_now_add=True, null=True)),
                ('nobets', models.FloatField(null=True, blank=True)),
                ('nowinners', models.FloatField(null=True, blank=True)),
                ('nolosers', models.FloatField(null=True, blank=True)),
                ('uniquewinners', models.FloatField(null=True, blank=True)),
                ('maxlosingsequence', models.IntegerField(null=True, blank=True)),
                ('avglosingsequence', models.IntegerField(null=True, blank=True)),
                ('maxwinningsequence', models.IntegerField(null=True, blank=True)),
                ('isLive', models.BooleanField()),
                ('a_e', models.FloatField()),
                ('year', models.IntegerField()),
                ('maxstake', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=2, blank=True)),
                ('avgstake', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=2, blank=True)),
                ('maxbalance', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=2, blank=True)),
                ('minbalance', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=2, blank=True)),
                ('individualrunners', models.FloatField(max_length=5)),
                ('wentLive', models.DateTimeField(null=True)),
                ('bfwinsr', models.FloatField(null=True, blank=True)),
                ('cashoutbalance', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=2, blank=True)),
                ('totalwinnings', models.DecimalField(default=Decimal('0'), max_digits=6, decimal_places=2, blank=True)),
                ('totalroi', models.FloatField(null=True, blank=True)),
            ],
            options={
                'get_latest_by': 'wentLive',
                'ordering': ['-totalwinnings'],
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'permissions': (('view_task', 'View task'),),
            },
        ),
        migrations.AlterUniqueTogether(
            name='fundaccount',
            unique_together=set([('fundname', 'description')]),
        ),
        migrations.AlterIndexTogether(
            name='fundaccount',
            index_together=set([('fundname', 'description')]),
        ),
    ]
