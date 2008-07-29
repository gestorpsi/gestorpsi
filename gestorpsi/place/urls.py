from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.place.views',
    (r'^$', 'index' ),
    (r'^(?P<object_id>\d+)/$', 'form'),
    (r'^add/$', 'add'),
    (r'^save/$', 'save'),
    (r'^delete/(\d+)$', 'delete'),
    (r'^get/(\d+)$', 'get'),
    (r'^update/(\d+)$', 'update'),
    (r'^add_room/(\d+)$', 'add_room'),
    (r'^save_room/$', 'save_room'),
    (r'^list_rooms/(\d+)$', 'list_rooms_related_to'),
    (r'^delete_room/(\d+)$', 'delete_room'),
    (r'^get_room/(\d+)$', 'get_room'),
    (r'^update_room/(\d+)$', 'update_room'),
)