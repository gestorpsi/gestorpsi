#!/usr/bin/env python
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

'''
    header file for script files
    set path : full path to project root folder
'''

import sys, locale, os
from datetime import datetime

reload(sys)
sys.setdefaultencoding("utf-8")
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# import Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'gestorpsi.settings.production'

# full path to Python libray
python_bin_path = os.popen("which python").read().strip()
sys.path.append(python_bin_path)

# full path to root Django project, manage.py
#TODO prevent errors when change the scripts folder structure, maybe check
# for manage.py file and raise an error if not found
path = os.path.realpath(__file__  + '/../../')

# append paths inside of project
sys.path.append('..')
sys.path.append("%s" % path)
sys.path.append("%s/scripts" % path)
sys.path.append("%s/gestorpsi" % path)

# print script filename and date to log
print
print "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # "
print "# %s " % sys.argv[0]
print "# %s " % datetime.today()
