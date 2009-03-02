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
from gestorpsi.settings import MEDIA_ROOT, PROJECT_ROOT_PATH
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from geraldo import ReportBand, BAND_WIDTH
from geraldo import Image, Line, Label, SystemField

def header_gen(organization, header_line=True, clinic_info=True):
    # Cannot use image thumbnail because it's too large (PROJECT_ROOT_PATH,pathdir,'.thumb',organization.photo)
    pathdir = '%simg/organization/%s' % (MEDIA_ROOT, organization.id)
    imagefile = os.path.join(PROJECT_ROOT_PATH,pathdir,'.thumb',organization.photo)
    class Header(ReportBand):
        height = 2.3*cm
        borders = {'bottom': False}
        elements = [
            SystemField(expression='%(report_title)s', top=1*cm, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica', 'fontSize': 12, 'alignment': TA_CENTER}),
            SystemField(expression='Printed in %(now:%d/%m/%Y %H:%M)s ', top=1.74*cm, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica', 'fontSize': 8, 'alignment': TA_LEFT}),
            SystemField(expression='Page %(page_number)d of %(page_count)d', top=1.74*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica', 'fontSize': 8, 'alignment': TA_RIGHT}),
        ]

        if clinic_info:
            elements.append(Label(text="%s" % organization, top=0.1*cm, left=0, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}))
            if len(organization.photo):
                elements.append(Image(left=0.1*cm, top=0.1*cm, filename=imagefile))

        if header_line:
            elements.append(Line(left=0.0*cm, right=19*cm, top=2*cm, bottom=2*cm))

    return Header()

