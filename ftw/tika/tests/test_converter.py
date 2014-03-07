from StringIO import StringIO
from ftw.testing import MockTestCase
from ftw.tika.converter import TikaConverter
from ftw.tika.exceptions import ProcessError
from ftw.tika.exceptions import TikaConversionError
from ftw.tika.exceptions import TikaJarNotConfigured
from ftw.tika.exceptions import TikaJarNotFound
from ftw.tika.interfaces import IZCMLTikaConfig
from ftw.tika.testing import FTW_TIKA_INTEGRATION_TESTING
from mocker import ARGS
from zope.component import getGlobalSiteManager
from zope.component import getUtility
import tempfile


class TestConverter(MockTestCase):

    layer = FTW_TIKA_INTEGRATION_TESTING

    def test_converter_builds_correct_command_line(self):
        # Patch run_process to just return stderr and the command line given

        def return_cmd_line(cmd):
            return (cmd, '')

        mock_run_proc = self.mocker.replace('ftw.tika.converter.run_process')
        self.expect(mock_run_proc(ARGS)).call(return_cmd_line)
        self.replay()

        jar_path = '/bin/ls'
        tika_converter = TikaConverter(path=jar_path)
        cmd = tika_converter.convert('')
        cmd_without_doc_filename = cmd.split()[:-1]

        self.assertEquals(cmd_without_doc_filename,
                          ['java', '-jar', jar_path, '-t'])

    def test_converter_accepts_file_like_stream_object(self):
        sample_text = 'TEXT'

        # Patch run_process to just return sample output
        mock_run_proc = self.mocker.replace('ftw.tika.converter.run_process')
        self.expect(mock_run_proc(ARGS)).result((sample_text, 'stderr'))
        self.replay()

        with tempfile.NamedTemporaryFile() as tmp_file:
            tika_converter = TikaConverter(path=tmp_file.name)
            plain_text = tika_converter.convert(StringIO(sample_text))

        self.assertEquals(plain_text, sample_text)

    def test_process_error_causes_coverter_to_raise_conversion_error(self):
        # Patch run_process to just raise a ProcessError

        def raise_process_error(cmd):
            raise ProcessError

        mock_run_proc = self.mocker.replace('ftw.tika.converter.run_process')
        self.expect(mock_run_proc(ARGS)).call(raise_process_error)
        self.replay()

        with tempfile.NamedTemporaryFile() as tmp_file:
            tika_converter = TikaConverter(path=tmp_file.name)
            with self.assertRaises(TikaConversionError):
                tika_converter.convert('')

    def test_missing_jar_path_causes_converter_to_raise(self):
        # Since the path is configured in the IZCMLTikaConfig from the ZCML
        # loaded in the testing layer, we need to unregister the config for
        # this test to verify the exception.
        config = getUtility(IZCMLTikaConfig)
        getGlobalSiteManager().unregisterUtility(provided=IZCMLTikaConfig)
        try:
            with self.assertRaises(TikaJarNotConfigured):
                TikaConverter().convert('')
        finally:
            getGlobalSiteManager().registerUtility(component=config)

    def test_invalid_jar_path_causes_converter_to_raise(self):
        tika_converter = TikaConverter(path="/nonexistent")
        with self.assertRaises(TikaJarNotFound):
            tika_converter.convert('')
