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

"""
SOMETHING_TYPE = (
    ('01', _('')),
    ('02', _('')),
    ('03', _('')),
    ('04', _('')),
    ('05', _('')),
    ('06', _('')),
    ('07', _('')),
    ('08', _('')),
)
"""

from django.utils.translation import ugettext_lazy as _

EDUCATION_LEVEL = (
    ('01', (u'Analfabeto')),
    ('02', (u'Até 4ª série incompleta (5º ano²) do ensino fundamental')),
    ('03', (u'Com 4ª série completa (5º ano²) do ensino fundamental')),
    ('04', (u'De 5ª à 8ª série incompleta (do 6º ao 9º ano²) do ensino fundamental')),
    ('05', (u'Ensino fundamental completo')),
    ('06', (u'Ensino médio incompleto')),
    ('07', (u'Ensino médio completo')),
    ('08', (u'Educação de Jovens e Adultos (EJA)')),
    ('09', (u'Curso pré-vestibular')),
    ('10', (u'Curso técnico')),
    ('11', (u'Curso profissionalizante')),
    ('12', (u'Superior incompleto')),
    ('13', (u'Superior completo')),
    ('14', (u'Especialização')),
    ('15', (u'Aprimoramento')),
    ('16', (u'Aperfeiçoamento')),
    ('17', (u'Mestrado')),
    ('18', (u'Doutorado')),
    ('19', (u'Pós-doutorado')),
)

TRANSPORTATION_TYPE = (
    ('01', _('Walking')),
    ('02', _('Bicycle')),
    ('03', _('Automobile')),
    ('04', _('Motorcycle')),
    ('05', _('Public transit: bus')),
    ('06', _('Public transit: subway')),
    ('07', _('Public transit: alternative transportation')),
    ('08', _('Public transit: train')),
    ('09', _('Adapted transport')),
    ('10', _('Taxi')),
    ('99', _('Others')),
)

INCOME_RANGE = (
    ('01',(u'Sem rendimento')),
    ('02',(u'Ate 1/2 salário mínimo')),
    ('03',(u'Mais de 1/2 a 1 salário mínimo')),
    ('04',(u'Mais de 1 a 2 salários mínimos')),
    ('05',(u'Mais de 2 a 3 salários mínimos')),
    ('06',(u'Mais de 3 a 5 salários mínimos')),
    ('07',(u'Mais de 5 a 10 salários mínimos')),
    ('08',(u'Mais de 10 a 20 salários mínimos')),
    ('09',(u'Mais de 20 salários mínimos')),
)

INCOME_SOURCE = (
    ('01',(u'Salário')),
    ('02',(u'Aposentadoria')),
    ('03',(u'Pensão')),
    ('04',(u'Aluguel')),
    ('05',(u'Pensão alimentícia, mesada, doação')),
    ('06',(u'Juros e dividendos de aplicações financeiras')),
    ('07',(u'Bolsa criança cidadã - PETI')),
    ('08',(u'Agente jovem')),
    ('09',(u'Bolsa escola')),
    ('10',(u'LOAS/BPC')),
    ('11',(u'Previdência Rural')),
    ('12',(u'PRONAF')),
    ('13',(u'PROGER')),
    ('14',(u'Seguro desemprego')),
    ('99',(u'Outra')),
)

POSSESSION_ITEMS = (
    ('01',_('Car')),
    ('02',_('Bathroom')),
    ('03',_('Monthly Employee')),
    ('04',_('Microwave oven')),
    ('05',_('Refrigerator')),
    ('06',_('Washing machine')),
    ('07',_('Phone line installed')),
    ('08',_('Computer')),
    ('09',_('Internet Broadband')),
    ('10',_('Internet Dial-up')),
    ('11',_('Motorcicle')),
    ('12',_('Radio')),
    ('13',_('Telvision')),
    ('14',_('Cable TV')),
    ('15',_('VCR / DVD')),
)

ELETRICITY_TYPE = (
    ('01', _('Individual meter')),
    ('02', _('No meter')),
    ('03', _('Shared meter')),
    ('04', _('Oil lamp')),
    ('05', _('Candlelight')),
    ('99', _('Other')),
)

WATER_SUPPLY_TYPE = (
    ('01', _('City water')),
    ('02', _('Well/spring')),
    ('03', _('Trucked in')),
    ('99', _('Other')),
)

WATER_SUPPLY_TREATMENT_TYPE = (
    ('01', _('Filtration')),
    ('02', _('Boiling')),
    ('03', _('Chlorination')),
    ('04', _('No treatment')),
    ('99', _('Other')),
)

SEWER_TYPE = (
    ('01', _('City sewer')),
    ('02', _('Rudimentar septic tank')),
    ('03', _('Septic tank')),
    ('04', _('Ditch')),
    ('05', _('Open air')),
    ('06', _('Stream, lake, ocean')),
    ('99', _('Other')),
)

WASTE_DISPOSITION_TYPE = (
    ('01', _('City collection')),
    ('02', _('Incinerated')),
    ('03', _('Enterred')),
    ('04', _('Open air')),
    ('05', _('Disposed off in appropriate container')),
    ('06', _('Disposed off irregularly (any place)')),
    ('07', _('Disposed off irregularly (stream, lake, ocean)')),
    ('99', _('Other')),
)

PAVIMENT_TYPE = (
    ('01',_('Asphalt')),
    ('02',_('Stone blocks')),
    ('03',_('Cement blocks')),
    ('99',_('Other')),
)

LOCATION_TYPE = (
    ('01',_('City dwelling')),
    ('02',_('Rural setting')),
)

SITUATION_TYPE = (
    ('01',_('Own')),
    ('02',_('Rent')),
    ('03',_('Leased')),
    ('04',_('Loaned')),
    ('05',_('Invasion')),
    ('06',_('Financed (has a mortgage)')),
    ('99',_('Other')),
)

DWELLING_TYPE = (
    ('01',_('Single family home')),
    ('02',_('Apartment')),
    ('03',_('Single room')),
    ('04',_('Collective')),
    ('05',_('Hotel')),
    ('06',_('Long term stay')),
    ('07',_('Jail')),
    ('08',_('Orphanage / Assisted living')),
    ('09',_('Hospital / Clinic')),
    ('99',_('Other')),
)

CONSTRUCTION_TYPE = (
    ('01',_('Stucko (brick)')),
    ('02',_('Adobe')),
    ('03',_('Protected taipa')),
    ('04',_('Unprotected taipa')),
    ('05',_('Wood')),
    ('06',_('Reused material')),
    ('99',_('Other')),
)

FLOOR_TYPE = (
    ('01',_('Hardwood')),
    ('02',_('Ceramic/tyle')),
    ('03',_('Carpet/vynil')),
    ('04',_('Concrete/dirt')),
    ('05',_('Reused wood')),
    ('06',_('Dirt')),
    ('07',_('Other')),
)

ROOF_TYPE = (
    ('01',_('Ceramic shingle')),
    ('02',_('Shingle')),
    ('03',_('Concrete')),
    ('04',_('Hardwood')),
    ('05',_('Aluminum')),
    ('06',_('Reused wood')),
    ('07',_('Straw')),
    ('99',_('Other')),
)

