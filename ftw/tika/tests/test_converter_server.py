from ftw.tika.converter import TikaConverter
from ftw.tika.testing import TIKA_SERVER_INTEGRATION_TESTING
from ftw.tika.utils import strip_word_bookmarks
from unittest2 import TestCase
import os.path


ASSETS = os.path.join(os.path.dirname(__file__), 'assets')


class TestServerConversion(TestCase):

    layer = TIKA_SERVER_INTEGRATION_TESTING

    def test_convert_docx(self):
        converter = TikaConverter()
        filename = 'lorem.docx'
        with open(os.path.join(ASSETS, filename)) as file_:
            result = converter.convert_server(file_)
        self.assertEquals(
            'Lorem Ipsum',
            strip_word_bookmarks(result.strip(), filename=filename))
