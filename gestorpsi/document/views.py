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

from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.address.models import State

# Check if documents fields are equals


def is_equal(document):
    try:
        document_db = Document.objects.get(pk=document.id)
    except:
        return False
    if cmp(document_db, document) == 0:
        return True
    else:
        return False

# Create a document list, but don't append blank documents


def document_list(
        ids, type_documents, documents, document_identifiers, issuers, states):
    objs = []
    for i in range(0, len(documents)):
        if (len(documents[i])):

            if len(type_documents[i]):
                td = TypeDocument.objects.get(pk=type_documents[i])
            else:
                td = None

            if len(issuers[i]):
                iss = Issuer.objects.get(pk=issuers[i])
            else:
                iss = None

            if len(states[i]):
                st = State.objects.get(pk=states[i])
            else:
                st = None

            objs.append(Document(
                id=ids[i], typeDocument=td, document=documents[i],
                document_identifier=document_identifiers[i], issuer=iss, state=st))

    return objs

# 'document' field blank means that it was deleted by an user
# So, if len(document) == 0 AND len(id) != 0, delete document using id


def document_delete(ids, documents):
    for i in range(0, len(documents)):
        if (not len(documents[i]) and len(ids[i])):
            Document.objects.get(pk=ids[i]).delete()

# def document_save(object, ids, type_documents, documents, issuers, states):
#    document_delete(ids, documents)
#    for document in document_list(ids, type_documents, documents, issuers, states):
#        if not is_equal(document):
#            document.content_object = object
#            document.save()


def document_save(object, ids, type_documents, documents,
                  document_identifiers, issuers, states):

    object.document.all().delete()
    for document in document_list(ids, type_documents, documents,
                                  document_identifiers, issuers, states):
        document.content_object = object
        document.save()
        