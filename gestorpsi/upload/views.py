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

import os
from django.http import HttpResponse  
from gestorpsi.settings import MEDIA_ROOT
import uuid
import Image


def send(request):
    if request.method == 'POST':
        user = request.user
        print user.org_active.id
        if 'file' in request.FILES:
            pathdir = '%simg/organization/%s' % (MEDIA_ROOT, user.org_active.id)
            if not os.path.exists(pathdir):
                os.mkdir(pathdir)
                os.mkdir('%s/.thumb' % pathdir)
                os.chmod(pathdir, 0777)
                os.chmod('%s/.thumb' % pathdir, 0777)
            file = request.FILES['file']
            print "TIPO DO ARQUIVO: %s" % file.content_type
            filename = str(uuid.uuid4()) + '.jpg'
            destination = open('%s/%s' % (pathdir,  filename), 'w+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

        
        #make thumb
        size = int(116), int(134)
        img = Image.open('%s/%s' % (pathdir, filename))
        img.thumbnail(size)
        img.save('%s/.thumb/%s' % (pathdir, filename))
        
        return HttpResponse('%s' % filename)


