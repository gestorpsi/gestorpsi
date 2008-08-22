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
def document_list(ids, typeDocuments, documents, issuers, states):
    objs = []
    for i in range(0, len(documents)):
        if (len(documents[i])):
            
            if len(typeDocuments[i]): td = TypeDocument.objects.get(pk=typeDocuments[i])
            else: td = None

            if len(issuers[i]): iss = Issuer.objects.get(pk=issuers[i])
            else: iss = None

            if len(states[i]): st = State.objects.get(pk=states[i])
            else: st = None

            objs.append(Document(id=ids[i], typeDocument=td, document=documents[i], issuer=iss, state=st))

    return objs

# 'document' field blank means that it was deleted by an user
# So, if len(document) == 0 AND len(id) != 0, delete document using id
def document_delete(ids, documents):
    for i in range(0, len(documents)):
        if (not len(documents[i]) and len(ids[i])):
            Document.objects.get(pk=ids[i]).delete()

def document_save(object, ids, typeDocuments, documents, issuers, states):
    document_delete(ids, documents)
    for document in document_list(ids, typeDocuments, documents, issuers, states):
        if not is_equal(document):
            document.content_object = object
            document.save()