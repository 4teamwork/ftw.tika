from Products.CMFCore.utils import getToolByName
from ftw.tika.interfaces import IZCMLTikaConfig
from ftw.tika.testing import FTW_TIKA_INTEGRATION_TESTING
from ftw.tika.testing import TIKA_SERVER_INTEGRATION_TESTING
from unittest2 import TestCase
from zope.component import getUtility
from zope.component.hooks import getSite
import os.path


ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
OFFICE_MIME = 'application/vnd.openxmlformats-officedocument.'
MIMETYPES_BY_EXTENSION = {
    '.docx': '%swordprocessingml.document' % OFFICE_MIME}


def convert_asset(filename):
    path = os.path.join(ASSETS, filename)
    transforms = getToolByName(getSite(), 'portal_transforms')
    _, extension = os.path.splitext(filename)
    mimetype = MIMETYPES_BY_EXTENSION[extension]
    with open(path, 'r') as asset:
        stream = transforms.convertTo('text/plain', asset, mimetype=mimetype)
        return stream.getData().strip()


class TestConversion(TestCase):

    layer = FTW_TIKA_INTEGRATION_TESTING

    def test_docx_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.docx'))


class TestServerConversion(TestCase):

    layer = TIKA_SERVER_INTEGRATION_TESTING

    def setUp(self):
        # Remove the tika path for disabling the local conversion fallback.
        # This allows us to detect when it could not be converted by the server.
        getUtility(IZCMLTikaConfig).path = None

    def test_docx_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.docx'))
