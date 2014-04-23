from Products.PortalTransforms.interfaces import ITransform
from ZODB.POSException import ConflictError
from ftw.tika import mimetypes
from ftw.tika.converter import TikaConverter
from ftw.tika.exceptions import TikaConversionError
from zope.interface import implements
import logging


TIKA_TRANSFORM_NAME = 'tika_to_plain_text'
INITIAL_TYPES = ['application/pdf']

logger = logging.getLogger('ftw.tika')


class Tika2TextTransform(object):
    """A portal transform that converts various office document formats to
    'text/plain' using Apache Tika.
    """

    implements(ITransform)

    __name__ = TIKA_TRANSFORM_NAME
    output = "text/plain"

    def __init__(self, name=None, inputs=INITIAL_TYPES):
        self.config = {'inputs': inputs}
        self.config_metadata = {
            'inputs': ('list', 'Inputs',
                       'Input(s) MIME type. Change with care.'),
            }
        if name:
            self.__name__ = name

    def name(self, *args):
        return self.__name__

    def __getattr__(self, attr):
        if attr in self.config:
            return self.config[attr]
        raise AttributeError(attr)

    def convert(self, orig, data, filename='', mimetype=None, **kwargs):
        converter = TikaConverter()
        try:
            plain_text = converter.convert(orig, filename=filename)

        except (ConflictError, KeyboardInterrupt):
            raise

        except TikaConversionError, exc:
            self._log_conversion_error(exc, mimetype=mimetype)
            plain_text = ''

        except Exception, exc:
            logger.warn(exc)
            plain_text = ''

        data.setData(plain_text)
        return data

    def _log_conversion_error(self, exc, mimetype):
        if ((mimetype in mimetypes.PDF_TYPES and
             self._is_pdf_protected_exception(exc))
            or (mimetype in mimetypes.MS_OFFICE_TYPES and
                self._is_msoffice_protected_exception(exc))):
            logger.info('Could not convert password protected document.')

        else:
            logger.warn(exc)

    def _is_pdf_protected_exception(self, exc):
        return ('Error: The supplied password does not match either the'
                ' owner or user password in the document.' in str(exc))

    def _is_msoffice_protected_exception(self, exc):
        return 'org.apache.tika.exception.EncryptedDocumentException' in str(exc)


def register():
    return Tika2TextTransform()
