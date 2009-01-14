from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from schedule import views

urlpatterns = patterns('gestorpsi.schedule.views',
#    url(r'^$', direct_to_template, { 'template': 'schedule/schedule_index.html'}, name='schedule-home'),
	(r'^$', include('swingtime.urls')),
    url(r'^swingtime/events/type/([^/]+)/$', 'event_type', name='karate-event'),
    (r'^swingtime/', include('swingtime.urls')),
)

