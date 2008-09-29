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
