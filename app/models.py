from django.db import models
from django.conf import settings
from django.utils.translation import get_language_info
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.signals import request_finished
from django.dispatch import receiver
from allauth.account import signals
from decimal import Decimal as D


en_en = get_language_info('en')['name_local']
de_de = get_language_info('de')['name_local']
zh_cn = get_language_info('zh-hans')['name_local']
zh_tw = get_language_info('zh-hant')['name_local']

class Investor(models.Model):

    LANGUAGES =(
                ('en-us', en_en),
                ('zh-cn', zh_cn),
                ('zh-tw', zh_tw),
                ('de-de', de_de),
                )

    user         = models.OneToOneField( settings.AUTH_USER_MODEL )
    language     = models.CharField(_('preferred language'), max_length=10, choices=LANGUAGES, default='en-us')
    GBPbalance   = models.DecimalField(blank=True,max_digits=6,decimal_places=2,default=D('0.00'))
    AUDbalance   = models.DecimalField(blank=True,max_digits=6,decimal_places=2,default=D('0.00'))

    def __unicode__(self):
        return '%s' % self.user
    

class Transaction( models.Model ):

    investor_from = models.ForeignKey   ( Investor, related_name = 'investor_from' )
    investor_to   = models.ForeignKey   ( Investor, related_name = 'investor_to'   )
    amount        = models.DecimalField ( max_digits = 6, decimal_places = 2 )
    currency      = models.CharField    ( max_length = 3, choices = settings.CURRENCIES )
    created       = models.DateTimeField( auto_now_add = True )


#create_transaction( investor_from, investor_to, currency, amount )


@receiver( signals.user_signed_up )
def on_user_created( sender, **kwargs ):

    Investor.objects.create( user = kwargs[ 'user' ] )

#signals.user_signed_up.connect( on_user_created )


