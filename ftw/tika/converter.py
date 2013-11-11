from ftw.tika.exceptions import ProcessError
from ftw.tika.exceptions import TikaConversionError
from ftw.tika.exceptions import TikaJarNotConfigured
from ftw.tika.exceptions import TikaJarNotFound
from ftw.tika.interfaces import IZCMLTikaConfig
from ftw.tika.utils import run_process
from zope.component import queryUtility
import logging
import os
import tempfile


class TikaConverter(object):
    """Converts documents to text/plain using Apache Tika.
    """

    def __init__(self, path=None):
        self._path = path
        self.log = logging.getLogger('ftw.tika')

    @property
    def java_path(self):
        return 'java'

    @property
    def jar_path(self):
        # Try path supplied to constructor first
        if self._path not in (None, ''):
            path = self._path
        else:
            # Otherwise try to get path from ZCML
            zcmlconfig = queryUtility(IZCMLTikaConfig)
            if zcmlconfig is not None:
                path = zcmlconfig.path
            else:
                # Bail if neither are provided
                msg = "No path to Tika JAR file specified."
                raise TikaJarNotConfigured(msg)

        # Check if the specified path is actually a file
        path = os.path.abspath(path)
        if not os.path.isfile(path):
            msg = "No such file: %s" % path
            raise TikaJarNotFound(msg)
        return path

    def convert(self, document, filename=''):
        """Converts `document` to 'text/plain' using Apache Tika.

        `document` can either be an string or a file-like stream object.
        """

        if not isinstance(document, basestring):
            # Treat it as a file-like stream object
            document = document.read()

        # Write the document in a temporary file
        doc_file = tempfile.NamedTemporaryFile(delete=False)
        doc_file.write(document)
        doc_file.close()

        cmd = ' '.join([self.java_path, '-jar', self.jar_path,
                        '-t', doc_file.name
                        ])

        self.log.info("Converting document '%s' with Tika..." % filename)
        try:
            stdout, stderr = run_process(cmd)
        except ProcessError, e:
            raise TikaConversionError(e.message)

        plain_text = stdout
        return plain_text
