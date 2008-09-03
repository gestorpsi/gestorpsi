# -*- coding: utf-8 -*-
from Crypto.Cipher import Blowfish
import binascii
from django.conf import settings

enc_obj= enc_obj= Blowfish.new(settings.SECRET_KEY)

def decrypt_attrib(attrib):
    """
    This helper function I{deciphers} C{attrib} and returns it as an unicode string.
    @type attrib: this variable probably is a C{CharField}
    @param attrib: the value to be deciphered
    @author: Vinicius H. S. Durelli
    """
    return u'%s' % ( enc_obj.decrypt(binascii.a2b_hex(attrib))).rstrip()
    
def encrypt_attrib(attrib):
    """
    This helper function I{encrypts} the value passed as parameter and returns the
    encrypted-value.
    @type attrib: this variable probably is a C{CharField}
    @param attrib: the value to be encrypted
    @author: Vinicius H. S. Durelli
    """
    repeat= 8 - (len(attrib) % 8)
    attrib= attrib + " " * repeat
    attrib= binascii.b2a_hex( enc_obj.encrypt(attrib))
    return attrib