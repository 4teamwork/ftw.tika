from ftw.tika.exceptions import TikaJarNotFound
from ftw.tika.testing import FtwTikaLayer
from plone.app.testing import FunctionalTesting
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
from zope.configuration import xmlconfig
import os


test_part_dir = os.getcwd()
test_jar_path = os.path.join(test_part_dir, 'tika-app.jar')


class FtwTikaZCMLDirectiveLayer(FtwTikaLayer):

    def setUpZope(self, app, configurationContext):
        super(FtwTikaZCMLDirectiveLayer, self).setUpZope(app,
                                                         configurationContext)
        # Load meta.zcml to register ZCML directive
        import ftw.tika
        xmlconfig.file('meta.zcml', ftw.tika,
                       context=configurationContext)

        # Set JAR path to our temp file using ZCML
        xmlconfig.string(
            '<configure xmlns:tika="http://namespaces.plone.org/tika">'
            '    <tika:config path="%s" />'
            '</configure>' % test_jar_path,
            context=configurationContext)


FTW_TIKA_ZCML_DIRECTIVE_FIXTURE = FtwTikaZCMLDirectiveLayer()
FTW_TIKA_ZCML_DIRECTIVE_FUNCTIONAL = FunctionalTesting(
    bases=(FTW_TIKA_ZCML_DIRECTIVE_FIXTURE,),
    name='FtwTika:FunctionalZCMLDirective')


class TestZCMLDirective(TestCase):

    layer = FTW_TIKA_ZCML_DIRECTIVE_FUNCTIONAL

    def test_transform_uses_path_set_by_zcml_directive(self):
        portal = self.layer['portal']
        transforms = getToolByName(portal, 'portal_transforms')

        # Monkey patch run_process helper
        from ftw.tika import converter
        _run_process = converter.run_process
        converter.run_process = lambda cmd: ('TEXT', 'stderr')

        # Create the file specified by the ZCML directive
        with open(test_jar_path, 'w'):
            stream = transforms.convertTo('text/plain',
                                          '',
                                          mimetype='application/pdf')
            plain_text = stream.getData()
        os.remove(test_jar_path)

        self.assertEquals(plain_text, 'TEXT')

        # Restore the original run_process function
        converter.run_process = _run_process

    def test_invalid_jar_path_in_zcml_doesnt_cause_transform_to_raise(self):
        portal = self.layer['portal']
        transforms = getToolByName(portal, 'portal_transforms')

        # DON'T create the file specified by the ZCML directive
        try:
            transforms.convertTo('text/plain',
                                 '',
                                 mimetype='application/pdf')
        except TikaJarNotFound, e:
            self.fail("transform raised '%s: %s' unexpectedly!" % (
                    e.__class__.__name__, e))
