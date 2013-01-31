# -*- coding: utf-8 -*-
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import Field
from django.utils.translation import ugettext_lazy as _
import re

def DV_maker(v):
	if v >= 2:
		return 11 - v
	return 0


class CPFField(Field):
	"""
	This field validate a CPF number or a CPF string. A CPF number is
	compounded by XXX.XXX.XXX-VD. The two last digits are check digits. If it fails it tries to validate a CNPJ number or a CNPJ string. A CNPJ is compounded by XX.XXX.XXX/XXXX-XX.

	More information:
	http://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas
	"""
	default_error_messages = {
		'invalid': _("Invalid CPF number."),
		'digits_only': _("This field requires only numbers."),
		'max_digits': _("This field requires at most 11 digits."),
	}

	def validate_CPF(self, value):
		"""
		Value can be either a string in the format XXX.XXX.XXX-XX or an
		11-digit number.
		"""
		if value in EMPTY_VALUES:
			return u''
		if not value.isdigit():
			value = re.sub("[-\.]", "", value)
		orig_value = value[:]
		try:
			int(value)
		except ValueError:
			raise ValidationError(self.error_messages['digits_only'])
		if len(value) != 11:
			raise ValidationError(self.error_messages['max_digits'])
		orig_dv = value[-2:]

		new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
		new_1dv = DV_maker(new_1dv % 11)
		value = value[:-2] + str(new_1dv) + value[-1]
		new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
		new_2dv = DV_maker(new_2dv % 11)
		value = value[:-1] + str(new_2dv)
		if value[-2:] != orig_dv:
			raise ValidationError(self.error_messages['invalid'])
		return orig_value
	
	def clean(self, value):
		value = super(CPFField, self).clean(value)
		orig_value = self.validate_CPF(value)
		return orig_value



class CNPJField(Field):
	"""
	This field validate a CPF number or a CPF string. A CPF number is
	compounded by XXX.XXX.XXX-VD. The two last digits are check digits. If it fails it tries to validate a CNPJ number or a CNPJ string. A CNPJ is compounded by XX.XXX.XXX/XXXX-XX.

	More information:
	http://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas
	"""
	default_error_messages = {
		'invalid': _("Invalid CNPJ number."),
		'digits_only': _("This field requires only numbers."),
		'max_digits': _("This field requires at most 14 digits."),
	}

	def validate_CNPJ(self, value):
		## Try to Validate CNPJ
		"""
		Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
		group of 14 characters.
		"""
		if value in EMPTY_VALUES:
			return u''
		if not value.isdigit():
			value = re.sub("[-/\.]", "", value)
		orig_value = value[:]
		try:
			int(value)
		except ValueError:
			raise ValidationError(self.error_messages['digits_only'])
		if len(value) != 14:
			raise ValidationError(self.error_messages['max_digits'])
		orig_dv = value[-2:]

		new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(5, 1, -1) + range(9, 1, -1))])
		new_1dv = DV_maker(new_1dv % 11)
		value = value[:-2] + str(new_1dv) + value[-1]
		new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(6, 1, -1) + range(9, 1, -1))])
		new_2dv = DV_maker(new_2dv % 11)
		value = value[:-1] + str(new_2dv)
		if value[-2:] != orig_dv:
			raise ValidationError(self.error_messages['invalid'])

		return orig_value
	

	def clean(self, value):
		value = super(CNPJField, self).clean(value)
		orig_value = self.validate_CNPJ(value)

		return orig_value