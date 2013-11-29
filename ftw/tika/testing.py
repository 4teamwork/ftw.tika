from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import Layer
from zope.configuration import xmlconfig


class UtilsLayer(Layer):
    """Bare bones layer for testing Plone agnostic utility functions.
    """


class FtwTikaLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import ftw.tika
        xmlconfig.file('configure.zcml', ftw.tika,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.tika:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_TIKA_FIXTURE = FtwTikaLayer()
FTW_TIKA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_TIKA_FIXTURE,),
    name="FtwTika:Integration")
FTW_TIKA_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_TIKA_FIXTURE,),
    name='FtwTika:Functional')


UTILS_LAYER = UtilsLayer()
