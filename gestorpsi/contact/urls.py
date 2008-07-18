from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.contact.views',
    # Example:    
    (r'^$', 'index'),
    (r'^add/$', 'add'),
    (r'^save/$', 'save'),   
    (r'^(?P<pID>\d+)$', 'details'),
    (r'^delete/(?P<pID>\d+)$', 'delete'),
    (r'^add_careProfessional/(\d+)$', 'add_careProfessional'),
    (r'^list_careProfessionals/(\d+)$', 'list_careProfessionals_related_to'),
)


