from django.conf.urls      import patterns
from django.conf.urls      import url
from app                   import views


urlpatterns = patterns( '',

   url( r'^$',          views.LandingView.as_view(),     name = 'landing'       ),
   url( r'^detail/$',   views.DetailView.as_view(),      name = 'detail'        ),
   url( r'^gbp/$',      views.GBPView.as_view(),         name = 'gbp'           ),
   url( r'^aud/$',      views.AUDView.as_view(),         name = 'aud'           ),
)


