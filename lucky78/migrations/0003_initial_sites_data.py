# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db              import migrations
from common.db.migrations   import migrations_load_fixture


def sites_import( apps, schema_editor ):
    migrations_load_fixture( apps, 'sitessite_initial.json' )
    migrations_load_fixture( apps, 'user_initial.json'      )


def sites_remove( apps, schema_editor ):
    apps.get_model( 'sites.site'   ).objects.all().delete()
    apps.get_model( 'auth.user'    ).objects.all().delete()

    
class Migration( migrations.Migration ):

    dependencies = [
        ( 'sites',    '0001_initial' ),
        ( 'auth',     '0006_require_contenttypes_0002'),
        ( 'guardian', '0001_initial' ),
    ]

    operations = [
        migrations.RunPython( sites_import, reverse_code = sites_remove )
    ]

