from django.conf                import settings
from django.http                import HttpResponseRedirect
from django.views               import generic
from django.utils.decorators    import method_decorator
from django.core.urlresolvers   import reverse
from guardian.shortcuts         import assign_perm
from guardian.shortcuts         import remove_perm
from decimal                    import Decimal
from .models                    import FundAccount, Investment
from app                        import logic
from app.models import Investor
from django.shortcuts           import (get_object_or_404,redirect, render)
import logging

logger = logging.getLogger(__name__)

def fundaccount_detail(request, slug):
    
    f = get_object_or_404(FundAccount, slug=slug)
    l_stats = ["bettingratio", "bfbalance", "openingbank", "totalinvested", "nobets", "nowinners", "nolosers","uniquewinners", 
    "maxlosingsequence", "avglosingsequence", "maxbalance", "a_e", "maxstake", "avgstake"]
    g_stats = ["managementfee", "performancefee", "bailoutfee", "stakescap", "performancethreshold", "paysDividends","nosystems", "isLive", "liveSince"]

    statslist = FundAccount.objects.values_list(*l_stats)
    statslist_d = { k: round(v,2) for k,v in zip(l_stats, statslist[0])}

    statslistg = FundAccount.objects.values_list(*g_stats)
    statslistg_d = { k: round(v,2) for k,v in zip(g_stats, statslist[0])}

    #fields for charts

    
    return render(request,'funds/fund.html', 
        {   
        'fund': f,
        'statslist': statslist_d,
        'genericstats': statslistg_d
        })


class FundAccountsView( generic.ListView ):

    template_name  = 'funds/funds.html'
    model          = FundAccount

    def get_context_data( self, **kwargs ):

        context = super( FundAccountsView, self ).get_context_data( **kwargs )
        investor = Investor.objects.get( user = self.request.user )

        context[ 'GBPbalance'     ] = investor.GBPbalance
        context[ 'AUDbalance'     ] = investor.AUDbalance
        context[ 'username'     ] =     self.request.user.username
        
        return context        




class FundAccountView( generic.DetailView ):

    template_name  = 'funds/fund.html'
    model          = FundAccount


    #get current live snapshot

    def getfundstats_generic( self, *args, **kwargs ):
        #get a dictionary of values with the following fields:
        #managementfee, performancefee, bailoutfee, stakecap, performancethreshold, paysDividends,
        #nosystems, isLive, livesince,
        self.fund = get_object_or_404(FundAccount, pk=self.args[0])


    def getfundstats_performance( self, *args, **kwargs ):
        #get a dictionary of values with the following fields:
        #bettingratio, bfbalance, openingbank, totalinvested, nobets, nowinners, nolosers,
        #uniquewinners, maxlosingsequence, avglosingsequence, maxbalance, a_e, maxstake, avgstake, 
        self.fund = get_object_or_404(FundAccount, pk=self.args[0])

    def getfieldsforcharts(self, *args, **kwargs ):
        pass
        #LINE CHARTS
        #x axis racedates
        #y axis: investments, 
        ## ???
        #x axis racedates? winpattern/placepattern 
        ##HISTOGRAM
        ##x axis racedates
        #y bars dailycashoutbalances, dailybfbalances, bfcumtotalbalances, fstartdaybalances_bfenddaybalances
        # cashedoutbalance??
    #accepts request returns a response
    def dispatch( self, *args, **kwargs ):
        return super( FundAccountView, self ).dispatch( *args, **kwargs )


'''
User can subscribe when:
sufficient funds in currency account
no already subscribed
messages
'''

class SubscribeView( generic.View ):

    def post( self, request, *args, **kwargs ):

        fundaccount = FundAccount.objects.get( pk = args[0] )
        investor    = Investor.objects.get( user = self.request.user  )
        admin       = Investor.objects.get( user__is_superuser = True )

        share = request.POST[ 'share' ].strip()
        if share != '':
            _share = Decimal( share )
            amount = (_share * Decimal( fundaccount.openingbank )) / Decimal('100.0')
            logger.info(fundaccount.openingbank)
            logger.info(amount)
            #
            if (fundaccount.currency == settings.CURRENCY_AUD and amount < investor.AUDbalance) or (fundaccount.currency == settings.CURRENCY_GBP and amount < investor.GBPbalance):
                
                transaction = logic.transfer( investor, admin, amount, fundaccount.currency )
                Investment.objects.create( transaction = transaction, fundaccount = fundaccount )
                assign_perm( 'view_task', request.user, fundaccount )

        # TODO: Here is place to create investment

        return HttpResponseRedirect( reverse( 'funds:fundaccounts' ) )


class UnsubscribeView( generic.View ):

    def get( self, request, *args, **kwargs ):
        ##unsubscribe if...
        fundaccount = models.FundAccount.objects.get( pk = args[0] )
        remove_perm( 'view_task', request.user, fundaccount )

        return HttpResponseRedirect( reverse( 'funds:fundaccounts' ) )

        