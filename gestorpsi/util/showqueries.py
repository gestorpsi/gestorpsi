from django.db import connection

class ShowQueries:

#    def process_request(self, request):
#        for q in connection.queries:
#            print "=============================================="
#            print q
#            print "=============================================="
#
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__module__ == 'gestorpsi.client.views':
            print "///////////////////////////////////////////////////"
            print "%s %s" % (view_func.__module__, view_func.__name__)
            print "///////////////////////////////////////////////////"

    def process_response(self, request, response):
        for q in connection.queries:
            print "=============================================="
            print q
            print "=============================================="
        return response