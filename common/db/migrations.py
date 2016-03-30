from django.core import serializers
from django.core import management

def migrations_load_fixture( apps, fixture ):

    # Monkey patching django core serializer to deserialize from history model while migrating
    old_get_model = serializers.python._get_model
    
    def _get_model( model_identifier ):
       return apps.get_model( model_identifier )

    serializers.python._get_model = _get_model

    management.call_command( "loaddata", fixture )
    
    serializers.python._get_model = old_get_model
