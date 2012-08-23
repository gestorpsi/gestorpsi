# -*- coding: utf-8 -*-

"""
Copyright (C) 2008 GestorPsi

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

"""
   This middleware shows all django generated sql 
   @author: Sergio Durand
   @version: 1.0
"""

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