from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.data import datastream
from Products.PortalTransforms.interfaces import ITransform
from ZODB.POSException import ConflictError
from ftw.testing import MockTestCase
from ftw.tika.exceptions import TikaJarNotConfigured
from ftw.tika.testing import FTW_TIKA_INTEGRATION_TESTING
from ftw.tika.tests.utils import RaisingConverter
from ftw.tika.transforms.tika_to_plain_text import Tika2TextTransform
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class TestTransforms(MockTestCase):

    layer = FTW_TIKA_INTEGRATION_TESTING

    def test_transform_conforms_to_interface(self):
        verifyClass(ITransform, Tika2TextTransform)

        transform = Tika2TextTransform(name='tika_to_plain_text')
        verifyObject(ITransform, transform)

    def test_transform_doesnt_raise_if_jar_path_missing(self):
        portal = self.layer['portal']
        transforms = getToolByName(portal, 'portal_transforms')

        try:
            transforms.convertTo('text/plain',
                                 '',
                                 mimetype='application/pdf')
        except TikaJarNotConfigured, e:
            self.fail("transform raised '%s: %s' unexpectedly!" % (
                    e.__class__.__name__, e))

    def test_transform_doesnt_swallow_conflict_errors(self):
        stream = datastream('dummy')

        # Patch TikaConverter class to just raise a ConflictError
        MockConverter = self.mocker.replace('ftw.tika.converter.TikaConverter')
        self.expect(MockConverter()).result(RaisingConverter(ConflictError))
        self.replay()

        transform = Tika2TextTransform()
        with self.assertRaises(ConflictError):
            transform.convert('', stream)

    def test_transform_doesnt_swallow_keyboard_interrupts(self):
        stream = datastream('dummy')

        # Patch TikaConverter class to just raise a ConflictError
        MockConverter = self.mocker.replace('ftw.tika.converter.TikaConverter')
        self.expect(MockConverter()).result(
            RaisingConverter(KeyboardInterrupt))
        self.replay()

        transform = Tika2TextTransform()
        with self.assertRaises(KeyboardInterrupt):
            transform.convert('', stream)
