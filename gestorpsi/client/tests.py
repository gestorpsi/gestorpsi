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

# ***********************************************************************
# FOR SOME REASON DJANGO IS NOT LOADING TESTS FROM INSIDE TEST FOLDER,
# THIS FILE IS A WORKAROUND TO MAINTAIN AN ORGANIZED STRUCTURE FOR TESTS
# THIS MAY BE SOLVED IN FUTURE DJANGO UPGRADES
# ***********************************************************************

from django.core.exceptions import ValidationError


#### MODELS ####
from .test.test_client import *

#### VIEWS ####

#### FORMS ####
