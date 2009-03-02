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

from gestorpsi.util.first_capitalized import first_capitalized
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from geraldo import ReportBand, BAND_WIDTH
from geraldo import SystemField

def footer_gen(organization):
    try:
        end = organization.address.all()[0]
        #line1 = "%s %s, %s - %s - %s - %s - %s" % (end.addressPrefix, end.addressLine1, end.addressNumber, end.addressLine2, end.neighborhood, first_capitalized(end.city.name), end.city.state.shortName)
        line1 = "%s %s, %s" % (end.addressPrefix, end.addressLine1, end.addressNumber)
        if len(end.addressLine2):
            line1 += " - %s" % end.addressLine2
        if len(end.neighborhood):
            line1 += " - %s" % end.neighborhood
        line1 += " - %s - %s" % (first_capitalized(end.city.name), end.city.state.shortName)
        line2 = "%s | %s | %s" % (organization.phones.all()[0], organization.sites.all()[0], organization.emails.all()[0])
        line3 = "CNPJ: %s | CNES: %s" % (organization.register_number, organization.cnes)
        class Footer(ReportBand):
            height = 0.5*cm
            borders = {'top': True}
            default_style = {'fontName': 'Helvetica', 'fontSize': 8, 'alignment': TA_CENTER}
            elements = [
                SystemField(expression=u'%s' % line1, top=0.1*cm, width=BAND_WIDTH),
                SystemField(expression=u'%s' % line2, top=0.4*cm, width=BAND_WIDTH),
                SystemField(expression=u'%s' % line3, top=0.7*cm, width=BAND_WIDTH), ]
    except:
        class Footer(ReportBand):
            height = 0.5*cm
            borders = {'top': True}

    return Footer()
