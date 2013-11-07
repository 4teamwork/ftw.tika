from ftw.tika.testing import FTW_TIKA_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase


class TestInstallation(TestCase):

    layer = FTW_TIKA_FUNCTIONAL_TESTING

    def test_default_profile_registers_transform(self):
        portal = self.layer['portal']
        portal_transforms = getToolByName(portal, 'portal_transforms')
        self.assertIn('tika_to_plain_text', portal_transforms.keys())

    def test_running_default_profile_twice_shouldnt_cause_errors(self):
        portal = self.layer['portal']
        setup_tool = getToolByName(portal, 'portal_setup')

        setup_tool.runAllImportStepsFromProfile('profile-ftw.tika:default',
                                                purge_old=False)

        # Running the uninstall profile twice shouldn't cause any errors
        setup_tool.runAllImportStepsFromProfile('profile-ftw.tika:default',
                                                purge_old=False)

