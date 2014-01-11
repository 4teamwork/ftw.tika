from ftw.tika.exceptions import ProcessError
from ftw.tika.exceptions import TikaConversionError
from ftw.tika.exceptions import TikaJarNotConfigured
from ftw.tika.exceptions import TikaJarNotFound
from ftw.tika.interfaces import IZCMLTikaConfig
from ftw.tika.utils import run_process
from plone.memoize import instance
from zope.component import queryUtility
import logging
import os
import socket
import tempfile


def copy_stream(input_, output):
    """Reads from the ``input_`` stream or string and writes into
    the ``output``. It does this in a buffered fashion for making
    sure that we never hold the whole file in our memory.

    This is used for copying the file data from Plone into either
    a tempfile when tika is used locally or into the socket which
    connects to the tika server.
    """
    if isinstance(input_, basestring):
        output.write(input_)
        return

    while True:
        data = input_.read(1024)
        if not data:
            break
        output.write(data)


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
    @instance.memoize
    def config(self):
        return queryUtility(IZCMLTikaConfig)

    @property
    def jar_path(self):
        # Try path supplied to constructor first
        if self._path not in (None, ''):
            path = self._path
        else:
            # Otherwise try to get path from ZCML
            if self.config is None or self.config.path is None:
                # Bail if neither are provided
                msg = "No path to Tika JAR file specified."
                raise TikaJarNotConfigured(msg)
            else:
                path = self.config.path

        # Check if the specified path is actually a file
        path = os.path.abspath(path)
        if not os.path.isfile(path):
            msg = "No such file: %s" % path
            raise TikaJarNotFound(msg)
        return path

    @property
    def server_configured(self):
        if self.config is None:
            return False
        return self.config.port is not None

    def convert(self, document, filename=''):
        """Converts `document` to 'text/plain' using Apache Tika.

        `document` can either be an string or a file-like stream object.
        """

        if self.server_configured:
            try:
                return self.convert_server(document, filename)
            except socket.error, exc:
                self.log.error('Could not connect to tika server: %s' % str(exc))

        return self.convert_local(document, filename)

    def convert_server(self, document, filename=''):
        self.log.info('Converting document with tika server: %s' % filename)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.config.host, self.config.port))
        input = sock.makefile()
        copy_stream(document, input)
        input.flush()
        sock.shutdown(socket.SHUT_WR)
        return input.read()

    def convert_local(self, document, filename=''):
        self.log.info('Converting document with LOCAL tika: %s' % filename)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        copy_stream(document, temp_file)
        temp_file.close()

        try:
            cmd = ' '.join([self.java_path, '-jar', self.jar_path,
                            '-t', temp_file.name])
            try:
                stdout, stderr = run_process(cmd)
            except ProcessError, e:
                raise TikaConversionError(e.message)
            return stdout

        finally:
            os.unlink(temp_file.name)
