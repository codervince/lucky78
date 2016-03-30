# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(default=b'en-us', max_length=10, verbose_name='preferred language', choices=[(b'en-us', 'English'), (b'zh-cn', '\u7b80\u4f53\u4e2d\u6587'), (b'zh-tw', '\u7e41\u9ad4\u4e2d\u6587'), (b'de-de', 'Deutsch')])),
                ('GBPbalance', models.DecimalField(default=Decimal('0.00'), max_digits=6, decimal_places=2, blank=True)),
                ('AUDbalance', models.DecimalField(default=Decimal('0.00'), max_digits=6, decimal_places=2, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('currency', models.CharField(max_length=3, choices=[(b'AUD', b'AUD'), (b'GBP', b'GBP')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('investor_from', models.ForeignKey(related_name='investor_from', to='app.Investor')),
                ('investor_to', models.ForeignKey(related_name='investor_to', to='app.Investor')),
            ],
        ),
    ]
