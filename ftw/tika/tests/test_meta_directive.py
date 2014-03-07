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
        self.load_zcml('<tika:config path="tika.jar" />')
        self.assertTrue(queryUtility(IZCMLTikaConfig),
                        'IZCMLTikaConfig utility should be registered after'
                        ' configuring it in ZCML.')

    def test_config_stores_path(self):
        self.load_zcml('<tika:config path="/path/to/tika.jar" />')
        config = getUtility(IZCMLTikaConfig)
        self.assertEquals('/path/to/tika.jar', config.path)

    def test_path_is_required(self):
        with self.assertRaises(ConfigurationError) as cm:
            self.load_zcml('<tika:config />')
        self.assertIn("('Missing parameter:', 'path')",
                      str(cm.exception))

    def load_zcml(self, *lines):
        self.layer.load_zcml_string('\n'.join((
                    '<configure xmlns:tika="http://namespaces.plone.org/tika">',
                    ) + lines +  (
                    '</configure>',
                    )))
