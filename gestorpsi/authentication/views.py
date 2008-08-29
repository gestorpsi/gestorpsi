from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect


def login_page(request):
    return render_to_response('registration/login.html')

def user_authentication(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)   
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response('core/main.html', {'user': user })       
    else:
            return render_to_response('registration/login.html', { 'message': "Invalid login" } )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login')
 