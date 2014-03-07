from ftw.tika.interfaces import IZCMLTikaConfig
from ftw.tika.testing import META_ZCML
from unittest2 import TestCase
from zope.component import getUtility
from zope.component import queryUtility
from zope.configuration.exceptions import ConfigurationError


class TestTikaConfigDirective(TestCase):

    layer = META_ZCML

    def test_no_config_utility_registered_when_not_configured(self):
        self.assertFalse(queryUtility(IZCMLTikaConfig),
                         'Expected IZCMLTikaConfig to not be registered yet.')

    def test_zcml_directive_registers_utility(self):
        self.load_zcml('<tika:config />')
        self.assertTrue(queryUtility(IZCMLTikaConfig),
                        'IZCMLTikaConfig utility should be registered after'
                        ' configuring it in ZCML.')

    def test_config_stores_path(self):
        self.load_zcml('<tika:config path="/path/to/tika.jar" />')
        config = getUtility(IZCMLTikaConfig)
        self.assertEquals('/path/to/tika.jar', config.path)

    def test_config_stores_port(self):
        self.load_zcml('<tika:config port="8077" />')
        config = getUtility(IZCMLTikaConfig)
        self.assertEquals(8077, config.port)

    def test_port_needs_to_be_integer(self):
        with self.assertRaises(ConfigurationError) as cm:
            self.load_zcml('<tika:config port="foo" />')
        self.assertIn('ValueError: invalid literal for int',
                      str(cm.exception))

    def test_config_stores_host(self):
        self.load_zcml('<tika:config host="other.host" />')
        config = getUtility(IZCMLTikaConfig)
        self.assertEquals('other.host', config.host)

    def test_host_defaults_to_localhost(self):
        self.load_zcml('<tika:config />')
        config = getUtility(IZCMLTikaConfig)
        self.assertEquals('localhost', config.host)

    def load_zcml(self, *lines):
        self.layer.load_zcml_string('\n'.join((
                    '<configure xmlns:tika="http://namespaces.plone.org/tika">',
                    ) + lines +  (
                    '</configure>',
                    )))
