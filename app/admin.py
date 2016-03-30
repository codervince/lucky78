from django                        import forms
from django.contrib                import admin
from django.contrib.admin.helpers  import ActionForm
from django.conf                   import settings
from decimal                       import Decimal
from app.models                    import Investor
from app.models                    import Transaction
from app                           import logic


class TransactionAdmin( admin.ModelAdmin ):

    list_display   = ( 'investor_from', 'investor_to', 'amount', 'currency', 'created', )


class TransferActionForm( ActionForm ):

    amountGBP = forms.DecimalField( max_digits = 6, decimal_places = 2, required = False )
    amountAUD = forms.DecimalField( max_digits = 6, decimal_places = 2, required = False )


class InvestorAdmin( admin.ModelAdmin ):

    list_display   = ( 'user', 'GBPbalance', 'AUDbalance', )
    action_form    = TransferActionForm

    def transfer( self, request, queryset ):

        amountGBP = request.POST[ 'amountGBP' ].strip()
        amountAUD = request.POST[ 'amountAUD' ].strip()

        admin = Investor.objects.get( user = request.user )

        for investor in queryset:

            if amountGBP != '':
                logic.transfer( admin, investor, Decimal( amountGBP ), settings.CURRENCY_GBP )

            if amountAUD != '':
                logic.transfer( admin, investor, Decimal( amountAUD ), settings.CURRENCY_AUD )


    transfer.short_description = 'Transfer'

    actions        = [ transfer ]


     


admin.site.register( Transaction,   TransactionAdmin      )
admin.site.register( Investor,      InvestorAdmin         )



