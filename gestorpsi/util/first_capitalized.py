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
This function was based on "Filter Capitalise Sentences"
Capsentence Author: djm
            Posted: January 27, 2009
              site: http://www.djangosnippets.org/snippets/1298/

Author: Sergio Durand - GestorPsi
Date: Feb 12, 2009
"""

def first_capitalized(text):
    value = text.lower()
    return " ".join([sentence.capitalize() for sentence in value.split(" ")])
