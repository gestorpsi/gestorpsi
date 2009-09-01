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
Cutom num_range template tag
Code from http://www.accountis.com/blog/?p=53
'''

from django.template import Library

register = Library()

@register.filter
def intequaltest(value, arg):
	return (value == int(arg))

@register.filter
def equaltest(value, arg):
	print arg
	return (value == arg)
