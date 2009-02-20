from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from gestorpsi.schedule import views

urlpatterns = patterns('gestorpsi.schedule.views',
    #url(r'^$', direct_to_template, { 'template': 'schedule/schedule_index.html'}, name='schedule-home'),
#    url(r'^swingtime/events/type/([^/]+)/$', 'event_type', name='karate-event'),
    url(r'^swingtime/', include('swingtime.urls')),
)
