# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db              import migrations
from common.db.migrations   import migrations_load_fixture


def investors_import( apps, schema_editor ):
    migrations_load_fixture( apps, 'investor_initial.json'  )


def investors_remove( apps, schema_editor ):
    apps.get_model( 'app.investor' ).objects.all().delete()

    
class Migration( migrations.Migration ):

    dependencies = [
        ( 'app',        '0001_initial' ),
        ( 'lucky78',    '0003_initial_sites_data' ),
    ]

    operations = [
        migrations.RunPython( investors_import, reverse_code = investors_remove )
    ]

