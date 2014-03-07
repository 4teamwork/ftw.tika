from ftw.tika.converter import TikaConverter
from ftw.tika.testing import FTW_TIKA_INTEGRATION_TESTING
from unittest2 import TestCase
import os.path


ASSETS = os.path.join(os.path.dirname(__file__), 'assets')


class TestLocalConversion(TestCase):

    layer = FTW_TIKA_INTEGRATION_TESTING

    def test_convert_docx(self):
        converter = TikaConverter()
        with open(os.path.join(ASSETS, 'lorem.docx')) as file_:
            result = converter.convert_local(file_)
        self.assertEquals('Lorem Ipsum', result.strip())
