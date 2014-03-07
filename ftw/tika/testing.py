from ftw.testing import ComponentRegistryLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from zope.configuration import xmlconfig
import os


class MetaZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(MetaZCMLLayer, self).setUp()
        import ftw.tika
        self.load_zcml_file('meta.zcml', ftw.tika)


META_ZCML = MetaZCMLLayer()


class FtwTikaLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import ftw.tika
        xmlconfig.file('configure.zcml', ftw.tika,
                       context=configurationContext)

        # os.getcwd() -> .../parts/test
        config = {'path': os.path.join(os.getcwd(), '..', 'tika', 'tika.jar')}

        xmlconfig.string(
            '<configure xmlns:tika="http://namespaces.plone.org/tika">' +
            '  <tika:config path="%(path)s" />' % config +
            '</configure>',
            context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.tika:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_TIKA_FIXTURE = FtwTikaLayer()
FTW_TIKA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_TIKA_FIXTURE,),
    name="FtwTika:Integration")
