from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.address.models import State

# append documents
def documentList(typeDocuments, documents, issuers, states):
    objs = []
    for i in range(0, len(documents)):
        if (len(documents[i])):
            
            if len(typeDocuments[i]): td = TypeDocument.objects.get(pk=typeDocuments[i])
            else: td = None

            if len(issuers[i]): iss = Issuer.objects.get(pk=issuers[i])
            else: iss = None

            if len(states[i]): st = State.objects.get(pk=states[i])
            else: st = None

            objs.append(Document(typeDocument=td, document=documents[i], issuer=iss, state=st))

    return objs

