# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

class UserTimeout:

#    def process_request(self, request):
#         print "ENTROU##################"
##         return HttpResponseRedirect('/') 
##         if (request.user.is_authenticated()):
##             print request.user.last_login         
#         if (request.session.get('flag') != None and request.user.is_anonymous()):
#             print "Ok"             
#             print "Limite"                  
#                     #return render_to_response('registration/login.html')
##         if (request.session.get('flag') == None):
##             if(request.user.is_anonymous()):
##                print "Limite"              
              
                 
    
    def process_view(self, request, view_func, view_args, view_kwargs):
         print "%s" % (view_func.__module__)
         if(view_func.__module__ != 'gestorpsi.authentication.views'):
             if(view_func.__module__ != 'gestorpsi.frontend.views'):                
                if(view_func.__module__ != 'django.views.static' ):                    
                    if (request.user.is_anonymous()):
                        return HttpResponseRedirect('/')                                        
                        print "///////////////////////////////////////////////////"
                        print "%s %s" % (view_func.__module__, view_func.__name__)
                        print "///////////////////////////////////////////////////"