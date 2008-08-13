from django.http import HttpResponse  
from gestorpsi.settings import MEDIA_ROOT
import uuid

def send(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            print "TIPO DO ARQUIVO: %s" % file.content_type
            filename = str(uuid.uuid4()) + '.jpg'
            destination = open('%simg/people/%s' % (MEDIA_ROOT, filename), 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
        return HttpResponse(filename)