from ftw.tika.interfaces import IZCMLTikaConfig
from zope import schema
from zope.component.zcml import utility
from zope.interface import implements
from zope.interface import Interface


class ZCMLTikaConfig(object):
    implements(IZCMLTikaConfig)

    def __init__(self, path):
        self.path = path


class ITikaConfigDirective(Interface):
    """Directive which registers a Tika config.
    """

    path = schema.ASCIILine(
        title=u"JAR Path",
        description=u"Path to the Tika JAR file.",
        required=True,
    )


def tikaConfigDirective(_context, path):
    """The <tika:config /> directive.
    Usage:

    <configure xmlns:tika="http://namespaces.plone.org/tika">
        <tika:config path="/usr/bin/tika" />
    </configure>
    """

    utility(_context,
            provides=IZCMLTikaConfig,
            component=ZCMLTikaConfig(path))
