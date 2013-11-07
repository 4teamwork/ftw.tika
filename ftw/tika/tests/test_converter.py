from ftw.tika.converter import TikaConverter
from ftw.tika.exceptions import ProcessError
from ftw.tika.exceptions import TikaConversionError
from ftw.tika.exceptions import TikaJarNotConfigured
from ftw.tika.exceptions import TikaJarNotFound
from ftw.tika.testing import FTW_TIKA_FUNCTIONAL_TESTING
from StringIO import StringIO
from unittest2 import TestCase
import tempfile


class TestConverter(TestCase):

    layer = FTW_TIKA_FUNCTIONAL_TESTING

    def test_converter_builds_correct_command_line(self):
        # Monkey patch run_process helper
        from ftw.tika import converter as _converter
        _run_process = _converter.run_process
        _converter.run_process = lambda cmd: (cmd, '')

        jar_path = '/bin/ls'
        tika_converter = TikaConverter(path=jar_path)
        cmd = tika_converter.convert('')
        cmd_without_doc_filename = cmd.split()[:-1]

        self.assertEquals(cmd_without_doc_filename,
                          ['java', '-jar', jar_path, '-t'])

        # Restore the original run_process function
        _converter.run_process = _run_process

    def test_converter_accepts_file_like_stream_object(self):
        sample_text = 'TEXT'

        # Monkey patch run_process helper
        from ftw.tika import converter as _converter
        _run_process = _converter.run_process
        _converter.run_process = lambda cmd: (sample_text, 'stderr')

        with tempfile.NamedTemporaryFile() as tmp_file:
            tika_converter = TikaConverter(path=tmp_file.name)
            plain_text = tika_converter.convert(StringIO(sample_text))

        self.assertEquals(plain_text, sample_text)

        # Restore the original run_process function
        _converter.run_process = _run_process

    def test_process_error_causes_coverter_to_raise_conversion_error(self):
        # Monkey patch run_process helper
        from ftw.tika import converter as _converter
        _run_process = _converter.run_process

        def raise_process_error(cmd):
            raise ProcessError

        _converter.run_process = raise_process_error

        with tempfile.NamedTemporaryFile() as tmp_file:

            with self.assertRaises(TikaConversionError):
                tika_converter = TikaConverter(path=tmp_file.name)
                _ = tika_converter.convert('')

        # Restore the original run_process function
        _converter.run_process = _run_process

    def test_missing_jar_path_causes_converter_to_raise(self):
        with self.assertRaises(TikaJarNotConfigured):
            tika_converter = TikaConverter()
            _ = tika_converter.convert('')

    def test_invalid_jar_path_causes_converter_to_raise(self):
        with self.assertRaises(TikaJarNotFound):
            tika_converter = TikaConverter(path="/nonexistent")
            _ = tika_converter.convert('')
