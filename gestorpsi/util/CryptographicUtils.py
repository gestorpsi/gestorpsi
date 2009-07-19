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

import binascii
from Crypto.Cipher import Blowfish
from django.conf import settings

enc_obj= enc_obj= Blowfish.new(settings.SECRET_KEY)

def decrypt_attrib(attrib):
    """
    This helper function I{deciphers} C{attrib} and returns it as an unicode string.
    @type attrib: this variable probably is a C{CharField}
    @param attrib: the value to be deciphered
    @author: Vinicius H. S. Durelli
    """
    return u'%s' % ( enc_obj.decrypt(binascii.a2b_hex(attrib))).rstrip().decode("utf-8")
    
def encrypt_attrib(attrib):
    """
    This helper function I{encrypts} the value passed as parameter and returns the
    encrypted-value.
    @type attrib: this variable probably is a C{CharField}
    @param attrib: the value to be encrypted
    @author: Vinicius H. S. Durelli
    """
    repeat= 8 - (len(attrib.encode("utf-8")) % 8)
    attrib= attrib + " " * repeat
    attrib= binascii.b2a_hex( enc_obj.encrypt(attrib.encode("utf-8")))
    return attrib