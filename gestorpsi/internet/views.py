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

from gestorpsi.internet.models import Email, EmailType, Site, InstantMessenger, IMNetwork

""" ************** Email section ************** """
def is_equal_email(email):
    try:
        email_db = Email.objects.get(pk=email.id)
    except:
        return False
    if cmp(email_db, email) == 0:
        return True
    else:
        return False

def email_list(ids, emails, emails_type):
    objs = []
    for i in range(0, len(emails)):
        if (len(emails[i])):            
            if len(emails_type[i]):
                et = EmailType.objects.get(pk=emails_type[i])
            else:
                et = None
            objs.append(Email(id=ids[i], email=emails[i], email_type=et))
    return objs

def email_delete(ids, emails):
    for i in range(0, len(emails)):
        if (not len(emails[i]) and len(ids[i])):
            Email.objects.get(pk=ids[i]).delete()

#def email_save(object, ids, emails, emails_type):
#    email_delete(ids, emails)
#    for email in email_list(ids, emails, emails_type):
#        if not is_equal_email(email):
#            email.content_object = object
#            email.save()

def email_save(object, ids, emails, emails_type):
    object.emails.all().delete()
    for email in email_list(ids, emails, emails_type):
        email.content_object = object
        email.save()

""" ************** Site section ************** """
def is_equal_site(site):
    try:
        site_db = Site.objects.get(pk=site.id)
    except:
        return False
    if cmp(site_db, site) == 0:
        return True
    else:
        return False

def site_list(ids, descriptions, sites):
    objs = []
    for i in range(0, len(sites)):
        if (len(sites[i])):
            objs.append(Site(id=ids[i], description=descriptions[i], site=sites[i]))
    return objs

def site_delete(ids, sites):
    for i in range(0, len(sites)):
        if (not len(sites[i]) and len(ids[i])):
            Site.objects.get(pk=ids[i]).delete()

#def site_save(object, ids, descriptions, sites):
#    site_delete(ids, sites)
#    for site in site_list(ids, descriptions, sites):
#        if not is_equal_site(site):
#            site.content_object = object
#            site.save()

def site_save(object, ids, descriptions, sites):
    object.sites.all().delete()
    for site in site_list(ids, descriptions, sites):
        site.content_object = object
        site.save()
            
""" ************** Instant Messenger section ************** """
def is_equal_im(im):
    try:
        im_db = InstantMessenger.objects.get(pk=im.id)
    except:
        return False
    if cmp(im_db, im) == 0:
        return True
    else:
        return False

def im_list(ids, identities, networks):
    objs = []
    for i in range(0, len(identities)):
        if (len(identities[i])):            
            if len(networks[i]):
                net = IMNetwork.objects.get(pk=networks[i])
            else:
                net = None
            objs.append(InstantMessenger(id=ids[i], identity=identities[i], network=net))
    return objs

def im_delete(ids, identities):
    for i in range(0, len(identities)):
        if (not len(identities[i]) and len(ids[i])):
            InstantMessenger.objects.get(pk=ids[i]).delete()

#def im_save(object, ids, identities, networks):
#    im_delete(ids, identities)
#    for im in im_list(ids, identities, networks):
#        if not is_equal_im(im):
#            im.content_object = object
#            im.save()

def im_save(object, ids, identities, networks):
    object.instantMessengers.all().delete()
    for im in im_list(ids, identities, networks):
        im.content_object = object
        im.save()
