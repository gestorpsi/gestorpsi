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
from gestorpsi.socioeconomic.choices import EDUCATION_LEVEL

LABOR_MARKET_STATUS = (
    ('01', _('Employer')),
    ('02', _('Legal employee (paying social security)')),
    ('03', _('Illegal employee')),
    ('04', _('Self employed paying social security')),
    ('05', _('Self employed not paying social security')),
    ('06', _('Retired')),
    ('07', _('Rural worker')),
    ('08', _('Rural employer (farm owner)')),
    ('09', _('Government employee')),
    ('10', _('Co-op / Intern')),
    ('11', _('Not working')),
    ('99', _('Other')),
)


