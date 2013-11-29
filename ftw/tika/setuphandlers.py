from ftw.tika.mimetypes import TYPES
from ftw.tika.transforms.tika_to_plain_text import Tika2TextTransform
from ftw.tika.transforms.tika_to_plain_text import TIKA_TRANSFORM_NAME
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.interfaces import IPortalTransformsTool
from Products.PortalTransforms.utils import TransformException
from zope.component import getUtility


# The profile id of your package:
PROFILE_ID = 'profile-ftw.tika:default'


class RegistrationUtility(object):
    """Handles registering and unregistering portal transforms and their
    policies.
    """

    def __init__(self, context, logger):
        self.context = context
        self.logger = logger

    def register_transform(self, transform):
        transform_tool = getUtility(IPortalTransformsTool)
        transform = transform()

        self.logger.info("Registering portal transform "
                         "'%s' " % transform.__name__)
        transform_tool.registerTransform(transform)

    def unregister_transform(self, transform_name):
        transform_tool = getUtility(IPortalTransformsTool)
        if hasattr(transform_tool, transform_name):
            self.logger.info("Unregistering portal transform "
                             "'%s' " % transform_name)
            transform_tool.unregisterTransform(transform_name)

    def register_transform_policy(self, output_mimetype, required_transform):
        transform_tool = getUtility(IPortalTransformsTool)
        transform_tool.manage_addPolicy(output_mimetype,
                                        [required_transform])

    def unregister_transform_policy(self, output_mimetype):
        transform_tool = getUtility(IPortalTransformsTool)
        policies = [mimetype for (mimetype, required)
                    in transform_tool.listPolicies()
                    if mimetype == output_mimetype]
        if policies:
            self.logger.info("Unregistering transform policy "
                             "for type '%s'" % output_mimetype)
            transform_tool.manage_delPolicies([output_mimetype])

    def filter_types_to_registered_ones_only(self, types):
        registry = getToolByName(self.context, 'mimetypes_registry')
        for mimetype in types:
            mts = registry.lookup(mimetype)
            if mts:
                yield mimetype

    def update_input_types(self, transform_name, types):
        transform_tool = getUtility(IPortalTransformsTool)
        transform = transform_tool[transform_name]
        transform.inputs = types[:]
        transform._config['inputs'] = types[:]
        # Update the portal_transform tool's internal _mtmap
        transform_tool._mapTransform(transform)
        self.logger.info(
            "Updated input types for transform '%s'." % transform_name)


def install_tika_policy(util, logger):
    """Install the transform policy for the tika_to_plain_text transform.

    If this policy is already present from an earlier install, remove and
    re-register it. If another policy for this output MIME type is present,
    bail with a decent error message.
    """

    output_mimetype = 'text/plain'
    required_transform = TIKA_TRANSFORM_NAME

    transform_tool = getUtility(IPortalTransformsTool)
    policies = [(mimetype, required) for (mimetype, required)
                in transform_tool.listPolicies()
                if mimetype == output_mimetype]

    if len(policies) == 1 and policies[0][1] == (required_transform, ):
        # That's our own policy (from a previous install)
        # Unregister it before registering it again
        util.unregister_transform_policy(output_mimetype)

    try:
        util.register_transform_policy(output_mimetype, TIKA_TRANSFORM_NAME)
    except TransformException:
        logger.error(
            "There is already a transform policy for '%s' installed! "
            "Please remove it first using the portal_transforms tool "
            "before attempting to install ftw.tika." % output_mimetype)

        raise TransformException(
            "A policy for 'text/plain' already exists - please uninstall "
            "it first if you want to install ftw.tika.")


# Handlers called with DirectoryImportContext by portal_setup tool

def install_portal_transforms(context):
    """Registers portal transforms for Tika integration.
    """
    if context.readDataFile('ftw.tika.default.txt') is None:
        return
    logger = context.getLogger('ftw.tika')
    site = context.getSite()

    util = RegistrationUtility(site, logger)
    util.register_transform(Tika2TextTransform)

    # Filter supported types to only those available in Plone's MIME type
    # registry in order to not cause exceptions during transform registration
    types = list(util.filter_types_to_registered_ones_only(TYPES))
    util.update_input_types(TIKA_TRANSFORM_NAME, types)

    install_tika_policy(util, logger)


def uninstall_portal_transforms(context):
    """Unregisters portal transforms for Tika integration.
    """
    if context.readDataFile('ftw.tika.uninstall.txt') is None:
        return
    logger = context.getLogger('ftw.tika')
    site = context.getSite()

    util = RegistrationUtility(site, logger)
    util.unregister_transform(TIKA_TRANSFORM_NAME)
    util.unregister_transform_policy("text/plain")
