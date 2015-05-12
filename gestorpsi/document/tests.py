from django.contrib.contenttypes.models import ContentType
from gestorpsi.document.models import Document, TypeDocument, Issuer
from gestorpsi.document.views import *

from django.test import TestCase


class DocumentViewsTest(TestCase):
    def setUp(self):
        self.typeDocument = TypeDocument(description="test")
        self.typeDocument.save()

        self.validDocumentName = "Valid Test Document"
        self.invalidDocumentName = "Invalid Test Document"

        self.validDocument = Document(typeDocument=self.typeDocument,
            document=self.validDocumentName)

        self.validDocument.content_type = ContentType.objects.get(
            app_label="document", model="Document")

        self.invalidDocument = Document(typeDocument=self.typeDocument,
            document=self.invalidDocumentName)

        self.invalidDocument.content_type = ContentType.objects.get(
            app_label="document", model="Document")

        self.validDocument.save()

    def testIsEqual(self):
        result = is_equal(self.validDocument)

        self.assertTrue(result)

    def testNotIsEqual(self):
        result = is_equal(self.invalidDocument)

        self.assertFalse(result)
