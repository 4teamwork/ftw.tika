from ftw.tika.testing import FTW_TIKA_FUNCTIONAL_TESTING
from unittest2 import TestCase


class TestInstallation(TestCase):

    layer = FTW_TIKA_FUNCTIONAL_TESTING

    def test_something(self):
        self.assertTrue(1==1)