# -*- coding: utf-8 -*-
# """
# Copyright (C) 2008 GestorPsi
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# """
#
# from PIL import Image as PILImage
# from reportlab.lib.units import cm
# from reportlab.lib.pagesizes import A4
# from geraldo import Report, ReportBand
# from geraldo import Image, Line, Label, ObjectValue
#
# class ClientListBandBegin(ReportBand):
#     height = 0.5*cm
#     default_style = {'fontName': 'Helvetica-Bold', 'fontSize': 10}
#     elements = [
#         Label(text="Name", top=0.1*cm, left=0),
#         Label(text="Birthdate", top=0.1*cm, left=11*cm),
#         Label(text="Phone", top=0.1*cm, left=15*cm), ]
#
# class ClientListBandDetail(ReportBand):
#     height = 0.5*cm
#     default_style = {'fontName': 'Helvetica', 'fontSize': 10}
#     elements = [
#         ObjectValue(attribute_name='person', top=0, left=0*cm, width=10*cm),
#         ObjectValue(top=0, left=11*cm, get_value=lambda instance: instance.person.get_birthdate()),
#         ObjectValue(top=0, left=15*cm, get_value=lambda instance: instance.person.get_first_phone()), ]
#
# class ClientList(Report):
#     page_size = A4
#     band_begin = ClientListBandBegin
#     band_detail = ClientListBandDetail
#     print_if_empty = True
#
# def client_record_gen(blocks):
#     class ClientRecordBandDetail(ReportBand):
#         top = 0.0*cm
#         def print_section(self):
#             retorno = self.top
#             self.top += 0.3*cm
#             return retorno
#
#         def print_line(self):
#             retorno = self.top
#             self.top += 0.2*cm
#             return retorno
#
#         def print_label(self):
#             retorno = self.top
#             self.top += 0.3*cm
#             return retorno
#
#         def print_content(self):
#             retorno = self.top
#             self.top += 0.7*cm
#             return retorno
#
#        height = 8.5*cm
#        label_style = {'fontName': 'Helvetica-Bold', 'fontSize': 8}
#        content_style = {'fontName': 'Helvetica', 'fontSize': 10}
#        elements = []
#
#        """ Code commented waiting a fix in Geraldo SubReport"""
#        #child_bands = [
#        #    ReportBand(
#        #        height = 0.5*cm,
#        #        borders={'bottom': True},
#        #        elements = [
#        #            Label(text="Documents", top=0.1*cm, left=0.5*cm, style=label_style),
#        #        ]
#        #    ),
#        #    ReportBand(
#        #        height = 0.5*cm,
#        #        borders={'bottom': True},
#        #        elements = [
#        #            Label(text="Phones", top=0.1*cm, left=0.5*cm, style=label_style),
#        #        ]
#        #    ),
#        #]
#
#    c = ClientRecordBandDetail()
#
#    """ Personal Indetification Block """
#    def block1():
#        c.elements.append(Label(text="Personal Identification", top=c.print_section(), left=0*cm, style=c.label_style))
#        c.elements.append(Line(left=0*cm, top=c.top, right=19*cm, bottom=c.print_line()))
#        c.elements.append(Image(left=14*cm, top=c.top, get_image=lambda graphic: PILImage.open('%s' % graphic.instance.person.get_photo())))
#        c.elements.append(Label(text="Name", top=c.print_label(), left=0, style=c.label_style))
#        c.elements.append(ObjectValue(top=c.print_content(), left=0*cm, get_value=lambda instance: instance.person.name, style=c.content_style))
#        c.elements.append(Label(text="Nickname", top=c.print_label(), left=0, style=c.label_style))
#        c.elements.append(ObjectValue(top=c.print_content(), left=0*cm, get_value=lambda instance: instance.person.nickname, style=c.content_style))
#        c.elements.append(Label(text="Gender", top=c.print_label(), left=0, style=c.label_style))
#        c.elements.append(ObjectValue(top=c.print_content(), left=0*cm, get_value=lambda instance: instance.person.get_gender_display(), style=c.content_style))
#
#    """ Personal Profile BLock """
#    def block2():
#        c.elements.append(Label(text="Personal Profile", top=c.print_section(), left=0*cm, style=c.label_style))
#        c.elements.append(Line(left=0*cm, top=c.top, right=19.0*cm, bottom=c.print_line()))
#        c.elements.append(Label(text="Birthdate", top=c.print_label(), left=0, style=c.label_style))
#        c.elements.append(ObjectValue(top=c.print_content(), left=0*cm, get_value=lambda instance: instance.person.get_birthdate(), style=c.content_style))
#        c.elements.append(Label(text="Marital Status", top=c.print_label(), left=0, style=c.label_style))
#        c.elements.append(ObjectValue(top=c.print_content(), left=0*cm, get_value=lambda instance: instance.person.maritalStatus, style=c.content_style))
#
#    """ Naturality Block """
#    def block3():
#        c.elements.append(Label(text="Naturality", top=c.print_section(), left=0*cm, style=c.label_style))
#        c.elements.append(Line(left=0*cm, top=c.top, right=19*cm, bottom=c.print_line()))
#        c.elements.append(Label(text="Country", top=c.print_label(), left=0, style=c.label_style))
#        c.elements.append(ObjectValue(top=c.print_content(), left=0*cm, get_value=lambda instance: instance.person.get_birth_country(), style=c.content_style))
#        c.elements.append(Label(text="City", top=c.print_label(), left=0, style=c.label_style))
#        c.elements.append(ObjectValue(top=c.print_content(), left=0*cm, get_value=lambda instance: instance.person.get_birth_place(), style=c.content_style))
#
#    """ Documents Block (waiting a fix in Geraldo SubReport) """
#    def block4():
#        c.elements.append(Label(text="Documents", top=c.print_section(), left=0*cm, style=c.label_style))
#        c.elements.append(Line(left=0*cm, top=c.top, right=19*cm, bottom=c.print_line()))
#        c.elements.append(ObjectValue(top=c.print_content(), width=10*cm, left=0*cm, get_value=lambda instance: instance.person.get_documents(), style=c.content_style))
#
#    """ Phones Block (waiting a fix in Geraldo SubReport) """
#    def block5():
#        c.elements.append(Label(text="Phones", top=c.print_section(), left=0*cm, style=c.label_style))
#        c.elements.append(Line(left=0*cm, top=c.top, right=19*cm, bottom=c.print_line()))
#        c.elements.append(ObjectValue(top=c.print_content(), width=10*cm, left=0*cm, get_value=lambda instance: instance.person.get_phones(), style=c.content_style))
#
#    """ Internet Block (waiting a fix in Geraldo SubReport) """
#    def block6():
#        pass
#        c.elements.append(Label(text="Internet Data", top=c.print_section(), left=0*cm, style=c.label_style))
#        c.elements.append(Line(left=0*cm, top=c.top, right=19*cm, bottom=c.print_line()))
#        c.elements.append(ObjectValue(top=c.print_content(), width=18*cm, left=0*cm, get_value=lambda instance: instance.person.get_internet(), style=c.content_style))
#
#    """ Addresses Block (waiting a fix in Geraldo SubReport) """
#    def block7():
#        c.elements.append(Label(text="Addresses", top=c.print_section(), left=0*cm, style=c.label_style))
#        c.elements.append(Line(left=0*cm, top=c.top, right=19*cm, bottom=c.print_line()))
#        c.elements.append(ObjectValue(top=c.print_content(), width=18*cm, left=0*cm, get_value=lambda instance: instance.person.get_address(), style=c.content_style))
#
#    # Print selected blocks
#    if blocks.count('block1'): block1()
#    if blocks.count('block2'): block2()
#    if blocks.count('block3'): block3()
#    if blocks.count('block4'): block4()
#    if blocks.count('block5'): block5()
#    if blocks.count('block6'): block6()
#    if blocks.count('block7'): block7()
#
#    return c
#
# class ClientRecord(Report):
#    page_size = A4
#    band_detail = client_record_gen(['block1', 'block2', 'block3', 'block4', 'block5', 'block6', 'block7'])
#    print_if_empty = True
#
#    """ Code commented waiting a fix in Geraldo SubReport"""
#    #subreports = [
#    #    SubReport(
#    #        queryset_string = '%(object)s.person.document.all()',
#    #        borders={'bottom': True},
#    #        detail_band = ReportBand(
#    #            height=0.5*cm,
#    #            elements=[
#    #                ObjectValue(attribute_name='__unicode__', top=0, left=0.5*cm),
#    #            ]
#    #        )
#    #    ),
#    #    SubReport(
#    #        queryset_string = '%(object)s.person.phones.all()',
#    #        borders={'bottom': True},
#    #        detail_band = ReportBand(
#    #            height=0.5*cm,
#    #            elements=[
#    #                ObjectValue(attribute_name='__unicode__', top=0, left=0.5*cm),
#    #            ]
#    #        )
#    #    ),
#    #]
