from ftw.tika.exceptions import ProcessError
from ftw.tika.exceptions import TikaConversionError
from ftw.tika.exceptions import TikaJarNotConfigured
from ftw.tika.exceptions import TikaJarNotFound
from ftw.tika.interfaces import IZCMLTikaConfig
from ftw.tika.utils import clean_extracted_plaintext
from ftw.tika.utils import run_process
from plone.memoize import instance
from requests.exceptions import RequestException
from StringIO import StringIO
from threading import local
from zope.component import queryUtility
import logging
import os
import requests
import socket
import tempfile


thread_locals = local()


def get_requests_session():
    attrname = 'tika_requests_session'
    if not hasattr(thread_locals, attrname):
        setattr(thread_locals, attrname, requests.session())
    return getattr(thread_locals, attrname)


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
                text = self.convert_server(document, filename)
            except (socket.error, RequestException), exc:
                self.log.error(
                    'Could not connect to tika server: %s' % str(exc))
                # Use local tika as fallback
                text = self.convert_local(document, filename)
        else:
            text = self.convert_local(document, filename)

        return text

    def convert_server(self, document, filename=''):
        base_url = "http://{0}:{1}".format(self.config.host, self.config.port)
        tika_endpoint = '/'.join((base_url, 'tika'))
        self.log.info(
            'Converting document with tika JAXRS server: %s' % filename)

        if isinstance(document, basestring):
            document = StringIO(document)

        headers = {'Accept': 'text/plain'}
        timeout = self.config.timeout
        response = get_requests_session().put(tika_endpoint,
                                              data=document,
                                              headers=headers,
                                              timeout=timeout)

        status, body = response.status_code, response.content

        if not status == 200:
            msg = ("Conversion with Tika JAXRS server failed "
                   "with status %s. " % status)
            raise TikaConversionError(
                msg, status_code=status, stack_trace=body.strip())

        text = clean_extracted_plaintext(body, filename)
        return text

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
                msg = "Conversion with local Tika failed."
                stack_trace = e.message
                raise TikaConversionError(msg, stack_trace=stack_trace)

            text = clean_extracted_plaintext(stdout, filename)
            return text

        finally:
            os.unlink(temp_file.name)
