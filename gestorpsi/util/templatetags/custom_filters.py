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