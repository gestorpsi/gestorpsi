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
from django.conf import settings
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from geraldo import ReportBand, BAND_WIDTH
from geraldo import Image, Line, Label, SystemField

def header_gen(organization, header_line=True, clinic_info=True):
    # Cannot use image thumbnail because it's too large (settings.PROJECT_ROOT_PATH,pathdir,'.thumb',organization.photo)
    pathdir = '%simg/organization/%s' % (settings.MEDIA_ROOT, organization.id)
    imagefile = os.path.join(settings.PROJECT_ROOT_PATH,pathdir,'.thumb-whitebg',organization.photo)
    class Header(ReportBand):
        height = 3.4*cm
        borders = {'bottom': False}
        elements = [
            SystemField(expression='%(report_title)s', top=1.9*cm, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica', 'fontSize': 12, 'alignment': TA_CENTER}),
            SystemField(expression='Page %(page_number)d of %(page_count)d', top=0.7*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica', 'fontSize': 8, 'alignment': TA_RIGHT}),
            SystemField(expression='Printed in %(now:%d/%m/%Y %H:%M)s ', top=0.2*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica', 'fontSize': 8, 'alignment': TA_RIGHT}),
        ]

        if clinic_info:
            elements.append(Label(text="%s" % organization, top=0.9*cm, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}))
            if len(organization.photo):
                elements.append(Image(left=0.1*cm, top=0.1*cm, filename=imagefile))

        if header_line:
            elements.append(Line(left=0.0*cm, right=19*cm, top=3.3*cm, bottom=3.3*cm))

    return Header()

