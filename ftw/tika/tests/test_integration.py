from ftw.tika.testing import FTW_TIKA_INTEGRATION_TESTING
from ftw.tika.testing import TIKA_SERVER_INTEGRATION_TESTING
from ftw.tika.testing import tika_version
from ftw.tika.tests.helpers import convert_asset
from testfixtures import log_capture
from unittest2 import TestCase


PROTECTED_MSG = (
    'ftw.tika', 'INFO', 'Could not convert password protected document.')


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

    @log_capture('ftw.tika')
    def test_protected_pdf_conversion(self, log):
        self.assertEquals('', convert_asset('protected.pdf'))
        self.assertIn(PROTECTED_MSG, tuple(log.actual()))

    @log_capture('ftw.tika')
    def test_protected_docx_conversion(self, log):
        self.assertEquals('', convert_asset('protected.docx'))
        self.assertIn(PROTECTED_MSG, tuple(log.actual()))


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

    @log_capture('ftw.tika')
    def test_protected_pdf_conversion(self, log):
        self.assertEquals('', convert_asset('protected.pdf'))
        if tika_version() >= (1, 8):
            self.assertIn(PROTECTED_MSG, tuple(log.actual()))
        else:
            # Assertion on status 422 doesn't work reliably - sometimes Tika
            # fails with a 500, sometimes with 422 (for the same test)
            self.assertIn(
                'Conversion with Tika JAXRS server failed with status',
                str(tuple(log.actual())))

    @log_capture('ftw.tika')
    def test_protected_docx_conversion(self, log):
        self.assertEquals('', convert_asset('protected.docx'))
        if tika_version() >= (1, 8):
            self.assertIn(PROTECTED_MSG, tuple(log.actual()))
        else:
            # Assertion on status 422 doesn't work reliably - sometimes Tika
            # fails with a 500, sometimes with 422 (for the same test)
            self.assertIn(
                'Conversion with Tika JAXRS server failed with status',
                str(tuple(log.actual())))
