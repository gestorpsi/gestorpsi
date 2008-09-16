from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.utils.translation import gettext as _
from gestorpsi.authentication.models import CustomUser
from gestorpsi.organization.models import Organization

def index(request):
    check_user()
    if(request.user.is_authenticated()):
        return render_to_response('core/main.html')
    else:
        return render_to_response('registration/login.html')
    
def check_user():    
    user = CustomUser.objects.all()
    if( len(user) < 1):
        ##Organization
        organization = Organization()
        organization.name = 'Organization_test_1'
        organization.active = True
        organization.save()
        
        #User
        user = CustomUser.objects.create_user('demo','demo@gestorpsi.com.br','demo')
        user.temp ='demo'
        user.organization.add(organization)
        user.save()
                
    else:
        print "There are " , len(user) , "users"
        

