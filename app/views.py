from django.views     import generic


class LandingView( generic.TemplateView ):
    template_name = 'app/landing.html'


class DetailView( generic.TemplateView ):
    template_name = 'app/detail.html'


class GBPView( generic.TemplateView ):
    template_name = 'app/gbp.html'


class AUDView( generic.TemplateView ):
    template_name = 'app/aud.html'
