from ftw.testing import ComponentRegistryLayer
from ftw.tika.interfaces import IZCMLTikaConfig
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import Layer
from subprocess import Popen
from threading import Thread
from zope.component import getUtility
from zope.configuration import xmlconfig
import os
import time


def tika_version():
    """Determine the Tika version we're testing against.
    """
    version = os.environ.get('TESTING_TIKA_VERSION', '0.0')
    return tuple(map(int, version.split('.')))


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
        parts_path = os.path.join(os.getcwd(), '..')

        app_path = os.path.join(
            parts_path, 'tika-app-download', 'tika-app.jar')
        self['tika_config'] = {'path': app_path,
                               'port': os.environ.get('PORT1', '55007')}

        xmlconfig.string(
            '<configure xmlns:tika="http://namespaces.plone.org/tika">' +
            '<tika:config path="%(path)s" />' % (
                self['tika_config']) +
            '</configure>',
            context=configurationContext)

        self['server_path'] = os.path.join(
            parts_path, 'tika-server-download', 'tika-server.jar')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.tika:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_TIKA_FIXTURE = FtwTikaLayer()
FTW_TIKA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_TIKA_FIXTURE,),
    name="FtwTika:Integration")


class TikaServerLayer(Layer):

    defaultBases = (FTW_TIKA_FIXTURE, )

    def setUp(self):
        self.start_server()

    def tearDown(self):
        self.stop_server()

    def testSetUp(self):
        # We explicitly remove the path for disabling fallback to
        # standalone method, so that we can make sure that the server
        # is actually used in this layer.
        tika_config = getUtility(IZCMLTikaConfig)
        tika_config.path = None
        tika_config.port = int(self['tika_config']['port'])

    def testTearDown(self):
        tika_config = getUtility(IZCMLTikaConfig)
        tika_config.path = self['tika_config']['path']
        tika_config.port = None

    def start_server(self):
        srv_config = {'server_path': self['server_path']}
        srv_config.update(self['tika_config'])

        additional_opts = []

        if tika_version() >= (1, 8):
            # Tika 1.8 allows to include the Java stack traces in the
            # response body for failed conversion requests.
            additional_opts.append('-includeStack')

        srv_config['additional_opts'] = ' '.join(additional_opts)

        command = ('java -jar %(server_path)s --port %(port)s '
                   '%(additional_opts)s' % (srv_config))

        self.process = Popen(command, shell=True)
        Thread(target=self.process.communicate).start()
        time.sleep(4.0)  # give tika some time to boot

    def stop_server(self):
        if getattr(self, 'process', None) is not None:
            self.process.terminate()

TIKA_SERVER_FIXTURE = TikaServerLayer()
TIKA_SERVER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TIKA_SERVER_FIXTURE,),
    name='FtwTika:server:Integration')
