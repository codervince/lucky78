# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Runner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('runtype', models.CharField(default=b'HISTORICAL', help_text='live_or_historical', max_length=15, choices=[(b'LIVE', b'LIVE'), (b'HISTORICAL', b'HISTORICAL')])),
                ('racedate', models.DateField(help_text='race date')),
                ('racecoursename', models.CharField(help_text='racecourse', max_length=35)),
                ('racecourseid', models.IntegerField(help_text='racecourseid', blank=True)),
                ('racename', models.CharField(help_text='race name', max_length=250)),
                ('racetypehorse', models.CharField(help_text='entry type horse', max_length=35)),
                ('racetypeconditions', models.CharField(help_text='entry conditions', max_length=35)),
                ('racetypehs', models.CharField(help_text='handicap or stakes', max_length=35)),
                ('ages', models.CharField(help_text='entry type ages', max_length=35)),
                ('oldraceclass', models.CharField(help_text='old raceclass', max_length=35)),
                ('newraceclass', models.CharField(help_text='new raceclass', max_length=35, blank=True)),
                ('distance', models.FloatField(help_text='distance furlongs')),
                ('going', models.CharField(help_text='going', max_length=35)),
                ('norunners', models.SmallIntegerField(help_text='number of runners')),
                ('horsename', models.CharField(help_text='horse name', max_length=250)),
                ('horseid', models.IntegerField(default=None, help_text='Horse id', blank=True)),
                ('sirename', models.CharField(help_text='sire name', max_length=250)),
                ('sireid', models.IntegerField(default=None, help_text='Sire id', blank=True)),
                ('trainername', models.CharField(help_text='trainer', max_length=250)),
                ('trainerid', models.IntegerField(default=None, help_text='Trainerid', blank=True)),
                ('jockeyname', models.CharField(help_text='jockey', max_length=250)),
                ('jockeyid', models.IntegerField(default=None, help_text='Jockey id', blank=True)),
                ('allowance', models.SmallIntegerField(help_text='jockey allowance')),
                ('finalpos', models.CharField(help_text='Final position', max_length=5)),
                ('lbw', models.FloatField(help_text='Beaten by L')),
                ('winsp', models.FloatField(help_text='final starting price win')),
                ('winsppos', models.SmallIntegerField(help_text='rank final starting price')),
                ('bfsp', models.DecimalField(help_text='Betfair SP win', max_digits=6, decimal_places=2)),
                ('bfpsp', models.DecimalField(help_text='Betfair SP place', max_digits=6, decimal_places=2)),
                ('fsratingrank', models.SmallIntegerField(help_text='FS Rating rank')),
                ('fsrating', models.FloatField(help_text='FS Rating')),
                ('fsraceno', models.CharField(help_text='distance', unique=True, max_length=250)),
                ('draw', models.SmallIntegerField(help_text='barrier')),
                ('damname', models.CharField(help_text="Dam's name", max_length=250)),
                ('damid', models.IntegerField(default=None, help_text='Dam id', blank=True)),
                ('damsirename', models.CharField(help_text="Dam's sire name", max_length=250)),
                ('damsireid', models.IntegerField(default=None, help_text='Dam sire id', blank=True)),
                ('ownerid', models.IntegerField(default=None, help_text='Owner id', blank=True)),
                ('racetime', models.CharField(help_text='Race off time', max_length=250)),
                ('totalruns', models.SmallIntegerField(help_text='total runs horse')),
                ('isplaced', models.BooleanField(help_text='Placed?')),
                ('isbfplaced', models.BooleanField(help_text='is Placed on Betfair?')),
            ],
            options={
                'ordering': ('-racedate',),
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('systemtype', models.CharField(default=b'tg', help_text='type: ', max_length=50, choices=[(b'tg', b'Trainglot'), (b'mi', b'Metainvest'), (b'custom', b'Custom'), (b'other', b'Other')])),
                ('systemname', models.CharField(help_text='system name', unique=True, max_length=50)),
                ('snapshotid', models.IntegerField()),
                ('description', models.TextField(help_text='rationale', blank=True)),
                ('isActive', models.BooleanField(default=True, help_text='active?')),
                ('isTurf', models.BooleanField(help_text='turf only?')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('snapshotid',),
            },
        ),
        migrations.CreateModel(
            name='SystemSnapshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('snapshottype', models.CharField(default=b'HISTORICAL', help_text='initial(historical/live) ', max_length=15, choices=[(b'LIVE', b'LIVE'), (b'HISTORICAL', b'HISTORICAL')])),
                ('bfwins', models.SmallIntegerField(default=None)),
                ('bfruns', models.SmallIntegerField(default=None)),
                ('winsr', models.FloatField(default=None)),
                ('expectedwins', models.FloatField(default=None)),
                ('a_e', models.FloatField(default=None)),
                ('levelbspprofit', models.DecimalField(default=None, max_digits=10, decimal_places=2)),
                ('levelbsprofitpc', models.FloatField(default=None)),
                ('a_e_last50', models.FloatField(default=None)),
                ('archie_allruns', models.FloatField(default=None)),
                ('expected_last50', models.FloatField(default=None)),
                ('archie_last50', models.FloatField(default=None)),
                ('last50wins', models.SmallIntegerField(default=None)),
                ('last50pc', models.FloatField(default=None)),
                ('last50str', models.CharField(default=None, max_length=250)),
                ('last28daysruns', models.SmallIntegerField(default=None)),
                ('profit_last50', models.DecimalField(default=None, max_digits=10, decimal_places=2)),
                ('longest_losing_streak', models.SmallIntegerField(default=None)),
                ('average_losing_streak', models.FloatField(default=None)),
                ('average_winning_streak', models.FloatField(default=None)),
                ('red_rows_ct', models.SmallIntegerField(default=None)),
                ('blue_rows_ct', models.SmallIntegerField(default=None)),
                ('green_rows_ct', models.SmallIntegerField(default=None)),
                ('total_rows_ct', models.SmallIntegerField(default=None)),
                ('red_rows_pc', models.FloatField(default=None)),
                ('blue_rows_pc', models.FloatField(default=None)),
                ('green_rows_pc', models.FloatField(default=None)),
                ('individualrunners', models.FloatField(default=None)),
                ('uniquewinners', models.FloatField(default=None)),
                ('uniquewinnerstorunnerspc', models.FloatField(default=None)),
                ('totalbackyears', models.SmallIntegerField(default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('runners', models.ManyToManyField(to='systems.Runner')),
                ('system', models.ForeignKey(related_name='systemsnapshot', to='systems.System')),
            ],
            options={
                'ordering': ('-levelbsprofitpc',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='runner',
            unique_together=set([('racedate', 'horsename')]),
        ),
    ]
