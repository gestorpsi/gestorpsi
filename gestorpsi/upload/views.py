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
        filename = ''
        if 'file' in request.FILES:
            pathdir = '%simg/organization/%s' % (MEDIA_ROOT, user.get_profile().org_active.id)
            print "PATHDIR %s" % pathdir
            if not os.path.exists(pathdir):
                os.mkdir(pathdir)
                os.mkdir('%s/.thumb' % pathdir)
                os.chmod(pathdir, 0777)
                os.chmod('%s/.thumb' % pathdir, 0777)
            file = request.FILES['file']
            try:
                if file.content_type in ['image/jpeg', 'image/png', 'image/gif']:
                    filename = str(uuid.uuid4()) + '.png'
                    destination = open('%s/%s' % (pathdir,  filename), 'w+')
                    for chunk in file.chunks():
                        destination.write(chunk)
                    destination.close()
                    im = Image.open('%s/%s' % (pathdir,  filename))
                    im.save('%s/%s' % (pathdir,  filename), "PNG")
    
                    # thumbnail 
                    img = Image.open('%s/%s' % (pathdir, filename))
                    size = img.size
                    
                    w = float(size[0])
                    h = float(size[1])
                   
                    if h/w < 1.155172414: # width > height
                        h = float(116) * h/w
                        w = 116
                    else:
                        w = float(134) * h/w
                        h = 134

                    img.thumbnail((int(w),int(h)), Image.ANTIALIAS)
                    
                    # put background
                    bg = Image.new('RGBA',(116,134), (0,0,0,0)) # light bg blue
                    W, H = bg.size
                    w, h = img.size
                    xo, yo = (W-w)/2, (H-h)/2
                    
                    # merge it
                    bg.paste(img, (xo, yo, xo+w, yo+h))
                    
                    # then save it
                    bg.save('%s/.thumb/%s' % (pathdir, filename), "PNG")
                    
            
            except IOError:
                print "error sending file"

        return HttpResponse('%s' % filename)
        


