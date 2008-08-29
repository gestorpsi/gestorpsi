from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.authentication.views',
    (r'^$', 'login_page'),    
    (r'^authentication', 'user_authentication'),
    (r'^logout', 'logout_page'),    
)