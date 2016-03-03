from ftw.tika.interfaces import IZCMLTikaConfig
from zope import schema
from zope.component.zcml import utility
from zope.interface import implements
from zope.interface import Interface


class ZCMLTikaConfig(object):
    implements(IZCMLTikaConfig)

    def __init__(self, path=None, port=None, host='localhost', timeout=10):
        self.path = path
        self.port = port
        self.host = host
        self.timeout = timeout


class ITikaConfigDirective(Interface):
    """Directive which registers a Tika config.
    """

    path = schema.ASCIILine(
        title=u"tika-app JAR Path",
        description=u"Path to the tika-app JAR file.",
        required=False,
    )

    port = schema.Int(
        title=u'Server port',
        description=u'The tika server port.',
        required=False)

    host = schema.ASCIILine(
        title=u"Server host",
        description=u'The tika server host.',
        required=False,
        )

    timeout = schema.Int(
        title=u'Connection Timeout',
        description=u'The timeout for the Connection to the tika server.',
        required=False,
        default=10)


def tikaConfigDirective(_context, **arguments):
    """The <tika:config /> directive.
    Usage:

    <configure xmlns:tika="http://namespaces.plone.org/tika">
        <tika:config path="/path/to/tika-app.jar"
                     host="tika.host"
                     port="9998"
                     timeout="10" />
    </configure>
    """

    utility(_context,
            provides=IZCMLTikaConfig,
            component=ZCMLTikaConfig(**arguments))
