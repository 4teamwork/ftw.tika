"""Utility functions for detecting password protected documents upon
conversion failure.
"""

from ftw.tika import mimetypes


PROTECTED_PDF_MSGS = (
    # Tika 1.5, 1.6
    'Error: The supplied password does not match either the'
    ' owner or user password in the document.',
    # Tika 1.7
    'Document is encrypted',
)

PROTECTED_MSOFFICE_MSGS = (
    # Tika 1.5, 1.6, 1.7
    'org.apache.tika.exception.EncryptedDocumentException',
)


def is_protected_doc(exc, mimetype):
    """Figure out whether conversion failed because we're dealing with
    a password protected document, based on the document's MIME type and
    the Java exception.
    """
    if mimetype in mimetypes.PDF_TYPES:
        return any(msg in str(exc) for msg in PROTECTED_PDF_MSGS)

    if mimetype in mimetypes.MS_OFFICE_TYPES:
        return any(msg in str(exc) for msg in PROTECTED_MSOFFICE_MSGS)

    return False
