from django.contrib import admin
from funds          import models


class FundAccountAdmin( admin.ModelAdmin ):

    list_display   = ( 'fundname', 'currency', )

class InvestmentAdmin( admin.ModelAdmin ):

    list_select_related = ( 'transaction', )
    list_display        = ( 'fundaccount', 'investor', 'amount', 'startdate' )

    def amount( self, obj ):
        return obj.transaction.amount

    def investor( self, obj ):
        return obj.transaction.investor_from

admin.site.register( models.FundAccount, FundAccountAdmin )
admin.site.register( models.Investment,  InvestmentAdmin  )