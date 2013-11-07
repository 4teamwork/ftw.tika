ftw.tika
========

This product integrates `Apache Tika <http://tika.apache.org/>`_ for full text indexing with **Plone** by
providing portal transforms to `text/plain` for the various document formats
supported by Tika.


Supported Formats
=================

Input Formats
-------------

* XML based Microsoft Office document formats

  - ``*.docx`` Word Documents
  - ``*.dotx`` Word Templates
  - ``*.xlsx`` Excel Sheets
  - ``*.xltx`` Excel Templates
  - ``*.pptx`` Powerpoint Presentations
  - ``*.potx`` Powerpoint Templates
  - ``*.ppsx`` Powerpoint Slideshows

See `mimetypes.py <https://github.com/4teamwork/ftw.tika/blob/master/ftw/tika/mimetypes.py>`_
for details on the MIME types corresponding to these formats.


Formats supported by Tika, but not wired up yet
------------------------------------------------

* Binary Microsoft Office document formats
* HyperText Markup Language
* XML and derived formats
* OpenDocument Format
* Portable Document Format
* Electronic Publication Format
* Rich Text Format
* Compression and packaging formats
* Text formats
* Audio formats
* Image formats
* Video formats
* Java class files and archives
* The mbox format

See the `Supported Document Formats <http://tika.apache.org/1.4/formats.html>`_
page on the Apache Tika Wiki for details.


Output Formats
--------------

* ``text/plain``


Installation
============

Dependencies
------------

``ftw.tika`` expects to be provided with the path to an installed Tika JAR
file. So install the ``tika-app.jar`` and pass the path to it to ``ftw.tika``,
either by passing it as a keyword argument when instanciating the converter
directly, or setting it in the Plone registry.

Installing ftw.tika
-------------------

- Install ``ftw.tika`` by adding it to the list of eggs in your buildout.
  Then run buildout and restart your instance:

.. code:: ini

    [instance]
    eggs +=
        ftw.tika


- Go to Site Setup of your Plone site and activate the ``ftw.tika`` add-on,
  or depend on the ``ftw.tika:default`` profile from your package's
  ``metadata.xml``.


Uninstalling ftw.tika
---------------------

``ftw.tika`` has an uninstall profile. To uninstall ``ftw.tika``, import the
``ftw.tika:uninstall`` profile using the ``portal_setup`` tool.


Compatibility
-------------

Plone 4.1

.. image:: https://jenkins.4teamwork.ch/job/ftw.tika-master-test-plone-4.1.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.tika-master-test-plone-4.1.x.cfg

Plone 4.2

.. image:: https://jenkins.4teamwork.ch/job/ftw.tika-master-test-plone-4.2.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.tika-master-test-plone-4.2.x.cfg

Plone 4.3

.. image:: https://jenkins.4teamwork.ch/job/ftw.tika-master-test-plone-4.3.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.tika-master-test-plone-4.3.x.cfg


Configuration
=============

``ftw.tika`` expects to be provided with a path to an installed
``tika-app.jar``. This can be done through ZCML, and therefore also
through buildout.


Configuration in ZCML
---------------------

The path to the Tika JAR file must be configured in ZCML.

If you used the supplied
`tika.cfg <https://github.com/4teamwork/ftw.tika/blob/master/tika.cfg>`_
as described above, you can reference the download location directly from
buildout by using ``${tika:destination}/${tika:filename}``:

.. code:: ini

    [instance]
    zcml-additional =
        <configure xmlns:tika="http://namespaces.plone.org/tika">
            <tika:config path="${tika:destination}/${tika:filename}" />
        </configure>

If you installed Tika yourself, just set ``path="/path/to/tika"`` accordingly.


Usage
=====

To use ``ftw.tika``, simply ask the ``portal_transforms`` tool for a
transformation to ``text/plain`` from one of the input formats supported by
``ftw.tika``:

.. code:: python

            namedfile = self.context.file
            transform_tool = getToolByName(self.context, 'portal_transforms')

            stream = transform_tool.convertTo(
                'text/plain',
                namedfile.data,
                mimetype=namedfile.contentType)
            plain_text = stream and stream.getData() or ''

The code calling Tika is encapsulated in its own class, so if for some reason
you don't want to use the ``portal_transforms`` tool, you can also use the
converter directly by just instanciating it:

.. code:: python

            from ftw.tika.converter import TikaConverter

            data = StringIO('foo')
            converter = TikaConverter(path="/path/to/tika.jar")
            plain_text = converter.convert(data)

The ``convert()`` method accepts either a data string or a file-like stream
object.


Links
=====

- Main github project repository: https://github.com/4teamwork/ftw.tika
- Issue tracker: https://github.com/4teamwork/ftw.tika/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.tika
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.tika
- Apache Tika: http://tika.apache.org


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.tika`` is licensed under GNU General Public License, version 2.
