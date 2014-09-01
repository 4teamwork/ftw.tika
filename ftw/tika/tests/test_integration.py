from ftw.tika.testing import FTW_TIKA_INTEGRATION_TESTING
from ftw.tika.testing import TIKA_SERVER_INTEGRATION_TESTING
from ftw.tika.tests.helpers import convert_asset
from unittest2 import TestCase


class TestConversion(TestCase):

    layer = FTW_TIKA_INTEGRATION_TESTING

    def test_docx_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.docx'))

    def test_doc_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.doc'))

    def test_xlsx_conversion(self):
        self.assertEquals('Sheet1\n\tLorem Ipsum',
                          convert_asset('lorem.xlsx'))

    def test_xls_conversion(self):
        self.assertEquals('Sheet1\n\tLorem Ipsum',
                          convert_asset('lorem.xls'))

    def test_pptx_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.pptx'))

    def test_ppt_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.ppt'))

    def test_pdf_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.pdf'))

    def test_rtf_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.rtf'))

    def test_odt_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.odt'))

    def test_sxw_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.sxw'))

    def test_eml_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.eml'))


class TestServerConversion(TestCase):

    layer = TIKA_SERVER_INTEGRATION_TESTING

    def test_docx_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.docx'))

    def test_doc_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.doc'))

    def test_xlsx_conversion(self):
        self.assertEquals('Sheet1\n\tLorem Ipsum',
                          convert_asset('lorem.xlsx'))

    def test_xls_conversion(self):
        self.assertEquals('Sheet1\n\tLorem Ipsum',
                          convert_asset('lorem.xls'))

    def test_pptx_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.pptx'))

    def test_ppt_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.ppt'))

    def test_pdf_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.pdf'))

    def test_rtf_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.rtf'))

    def test_odt_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.odt'))

    def test_sxw_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.sxw'))

    def test_eml_conversion(self):
        self.assertEquals('Lorem Ipsum', convert_asset('lorem.eml'))
