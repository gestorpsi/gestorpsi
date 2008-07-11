from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.places.views.',
    (r'^places/$', 'index' ),
    (r'^places/add/$', 'add'),
    (r'^places/save/$', 'save'),
    (r'^places/delete/(\d+)$', 'delete'),
    (r'^places/get/(\d+)$', 'get'),
    (r'^places/update/(\d+)$', 'update'),
    (r'^places/add_room/(\d+)$', 'add_room'),
    (r'^places/save_room/$', 'save_room'),
    (r'^places/list_rooms/(\d+)$', 'list_rooms_related_to'),
    (r'^places/delete_room/(\d+)$', 'delete_room'),
    (r'^places/get_room/(\d+)$', 'get_room'),
    (r'^places/update_room/(\d+)$', 'update_room'),
)