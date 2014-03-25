from ftw.tika.testing import FTW_TIKA_INTEGRATION_TESTING
from ftw.tika.testing import TIKA_SERVER_INTEGRATION_TESTING
from ftw.tika.tests.helpers import convert_asset
from unittest2 import TestCase



class TestConversion(TestCase):

    layer = FTW_TIKA_INTEGRATION_TESTING

    def test_docx_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.docx'))


class TestServerConversion(TestCase):

    layer = TIKA_SERVER_INTEGRATION_TESTING

    def test_docx_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.docx'))
