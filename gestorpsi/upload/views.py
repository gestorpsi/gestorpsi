#Create your views here.

from django import http  
from django import newforms as forms
from django.http import HttpResponse
from django.shortcuts import render_to_response  
from gestorpsi.settings import MEDIA_ROOT  
   
    
def send(request):  
	if request.method == 'POST':
		if 'file' in request.FILES:
			file = request.FILES['file']  
			filesize = len(file['content'])
			filetype = file['content-type']
			filename = file['filename']  
			fd = open('%s/img/people/%s' % (MEDIA_ROOT, filename), 'wb')  
			fd.write(file['content'])  
			fd.close()
		return HttpResponse(filename);
