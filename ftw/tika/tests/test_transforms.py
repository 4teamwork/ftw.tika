from ftw.tika.exceptions import TikaJarNotConfigured
from ftw.tika.testing import FTW_TIKA_FUNCTIONAL_TESTING
from ftw.tika.testing import SOME_MIMETYPE
from ftw.tika.transforms.tika_to_plain_text import Tika2TextTransform
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.interfaces import ITransform
from unittest2 import TestCase
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class TestTransforms(TestCase):

    layer = FTW_TIKA_FUNCTIONAL_TESTING

    def test_transform_conforms_to_interface(self):
        verifyClass(ITransform, Tika2TextTransform)

        transform = Tika2TextTransform(name='tika_to_plain_text')
        verifyObject(ITransform, transform)

    def test_transform_raises_if_jar_path_missing(self):
        portal = self.layer['portal']
        transforms = getToolByName(portal, 'portal_transforms')

        with self.assertRaises(TikaJarNotConfigured):
            _ = transforms.convertTo('text/plain', '', mimetype=SOME_MIMETYPE)
