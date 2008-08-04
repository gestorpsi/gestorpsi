from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.place.views',
    (r'^$', 'index'), # list objects
    (r'^add/$', 'form'), # new object form
    (r'^(?P<object_id>\d+)/$', 'form'), # edit object form
    (r'^save/$', 'save'), # save new object
    (r'^(?P<object_id>\d+)/save/$', 'save'), # update object
    (r'^delete/(\d+)$', 'delete'), # delete object
    (r'^get/(\d+)$', 'get'),
    (r'^add_room/(\d+)$', 'add_room'),
    (r'^save_room/$', 'save_room'),
    (r'^list_rooms/(\d+)$', 'list_rooms_related_to'),
    (r'^delete_room/(\d+)$', 'delete_room'),
    (r'^get_room/(\d+)$', 'get_room'),
    (r'^update_room/(\d+)$', 'update_room'),
)