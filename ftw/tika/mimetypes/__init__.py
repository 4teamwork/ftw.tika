"""MIME types supported by ftw.tika.

If you update any type definitions in here, please make sure you also update
the README accordingly.
"""

PDF_TYPES = [
    # PDF documents
    'application/pdf',
    'application/x-pdf',
    'image/pdf',
    'application/x-gzpdf',
    'application/x-bzpdf',
    'application/postscript',
    'application/x-gzpostscript',
    ]


TYPES = [
# Microsoft Office formats (Office Open XML)
'application/vnd.openxmlformats-officedocument.presentationml.presentation',
'application/vnd.openxmlformats-officedocument.presentationml.slide',
'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
'application/vnd.openxmlformats-officedocument.presentationml.template',
'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
'application/vnd.openxmlformats-officedocument.wordprocessingml.template',

# OpenOffice ODF formats
'application/vnd.oasis.opendocument.chart',
'application/vnd.oasis.opendocument.chart-template',
'application/vnd.oasis.opendocument.database',
'application/vnd.oasis.opendocument.formula',
'application/vnd.oasis.opendocument.formula-template',
'application/vnd.oasis.opendocument.graphics',
'application/vnd.oasis.opendocument.graphics-template',
'application/vnd.oasis.opendocument.image',
'application/vnd.oasis.opendocument.image-template',
'application/vnd.oasis.opendocument.presentation',
'application/vnd.oasis.opendocument.presentation-template',
'application/vnd.oasis.opendocument.spreadsheet',
'application/vnd.oasis.opendocument.spreadsheet-template',
'application/vnd.oasis.opendocument.text',
'application/vnd.oasis.opendocument.text-master',
'application/vnd.oasis.opendocument.text-template',
'application/vnd.oasis.opendocument.text-web',

# OpenOffice 1.x formats
'application/vnd.sun.xml.calc',
'application/vnd.sun.xml.calc.template',
'application/vnd.sun.xml.draw',
'application/vnd.sun.xml.draw.template',
'application/vnd.sun.xml.impress',
'application/vnd.sun.xml.impress.template',
'application/vnd.sun.xml.math',
'application/vnd.sun.xml.writer',
'application/vnd.sun.xml.writer.global',
'application/vnd.sun.xml.writer.template',

# Legacy Microsoft Office (97) formats
'application/vnd.ms-excel',
'application/msexcel',
'application/x-msexcel',
'application/vnd.ms-powerpoint',
'application/powerpoint',
'application/mspowerpoint',
'application/x-mspowerpoint',
'application/vnd.ms-works',
'application/msword',
'application/msword-template',
'application/rtf',
'application/vnd.visio',
'application/vnd.ms-tnef',
'application/ms-tnef',

# Adobe formats
'application/x-indesign',
'application/illustrator',
'image/x-photoshop',

# Other office formats
'application/vnd.wordperfect',
'application/x-wordperfect',
'application/wordperfect',

# E-Mail messages
'message/rfc822',
] + PDF_TYPES


MS_OFFICE_TYPES = [
    mt for mt in TYPES
    if mt.startswith('application/vnd.openxmlformats-officedocument.')]
