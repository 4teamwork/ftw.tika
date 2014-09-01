ftw.tika
========

This product integrates `Apache Tika <http://tika.apache.org/>`_ for full text
indexing with **Plone** by providing portal transforms to ``text/plain`` for the
various document formats supported by Tika.


Supported Formats
=================

Input Formats
-------------

* Microsoft Office formats (Office Open XML)

  - ``*.docx`` Word Documents
  - ``*.dotx`` Word Templates
  - ``*.xlsx`` Excel Sheets
  - ``*.xltx`` Excel Templates
  - ``*.pptx`` Powerpoint Presentations
  - ``*.potx`` Powerpoint Templates
  - ``*.ppsx`` Powerpoint Slideshows

* Legacy Microsoft Office (97) formats
* Rich Text Format
* OpenOffice ODF formats
* OpenOffice 1.x formats
* Common Adobe formats (InDesign, Illustrator, Photoshop)
* PDF documents
* WordPerfect documents
* E-Mail messages


See the `mimetypes <https://github.com/4teamwork/ftw.tika/blob/master/ftw/tika/mimetypes/__init__.py>`_
module for details on the MIME types corresponding to these formats.


Formats supported by Tika, but not wired up (yet)
-------------------------------------------------

* Electronic Publication Format
* Compression and packaging formats
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

The preferred method to run the Tika JAX-RS server as a daemon. Although it is
possible to run Tika without a daemon (by booting it up for each time a file
is converted), the daemon is a lot faster.

Both methods require ``tika-app.jar`` to be downloaded and some ZCML
configuration for ``ftw.tika``. The daemon method also requires the JAX-RS
``tika-server.app`` to be downloaded.

Below are some configuration examples.

Daemon buildout example
-----------------------

See the included `tika.cfg`_ for a deamon example that you can adjust as
necessary, copy into your buildout and extend from:

.. code:: ini

    [buildout]
    parts +=
        tika-app-download
        tika-server-download
        tika-server

    [tika]
    server-port = 9998
    zcml =
        <configure xmlns:tika="http://namespaces.plone.org/tika">
            <tika:config path="${tika-app-download:destination}/${tika-app-download:filename}"
                         port="${tika:server-port}" />
        </configure>

    [tika-app-download]
    recipe = hexagonit.recipe.download
    url = http://repo1.maven.org/maven2/org/apache/tika/tika-app/1.5/tika-app-1.5.jar
    md5sum = 2124a77289efbb30e7228c0f7da63373
    download-only = true
    filename = tika-app.jar

    [tika-server-download]
    recipe = hexagonit.recipe.download
    url = http://repo1.maven.org/maven2/org/apache/tika/tika-server/1.5/tika-server-1.5.jar
    md5sum = 0f70548f233ead7c299bf7bc73bfec26
    download-only = true
    filename = tika-server.jar

    [tika-server]
    recipe = collective.recipe.scriptgen
    cmd = java
    arguments = -jar ${tika-server-download:destination}/${tika-server-download:filename} --port ${tika:server-port}

    [instance]
    zcml-additional = ${tika:zcml}
    eggs += ftw.tika


If your deployment buildout is based on the deployment buildouts included
in the `ftw-buildouts`_ repository on github, you can simply extend the
``tika-jaxrs-server.cfg`` and you have everything configured:

.. code:: ini

    [buildout]
    extends =
        https://raw.github.com/4teamwork/ftw-buildouts/master/production.cfg
        https://raw.github.com/4teamwork/ftw-buildouts/master/zeoclients/4.cfg
        https://raw.github.com/4teamwork/ftw-buildouts/master/tika-jaxrs-server.cfg

    deployment-number = 05

    filestorage-parts =
        www.mywebsite.com

    instance-eggs =
        mywebsite


Non-daemon buildout example
---------------------------

Note that running Tika in non-daemon mode is very, very slow!

When you don't want to use Tika as daemon, you can simply just configure
the path to the ``tika-app.jar`` in the ``ftw.tika`` ZCML configuration and it
will fire up ``tika-app.jar`` (in a new JVM) every time something needs to be
converted.

Here is a short example of how to download the ``tika-app.jar`` and
configuring ``ftw.tika`` with buildout:

.. code:: ini

    [buildout]
    parts +=
        tika-app

    [tika-app]
    recipe = hexagonit.recipe.download
    url = http://repo1.maven.org/maven2/org/apache/tika/tika-app/1.6/tika-app-1.6.jar
    md5sum = 2d8af1f228000fcda92bd0dda20b80a8
    download-only = true
    filename = tika-app.jar

    [instance]
    eggs += ftw.tika
    zcml-additional =
        <configure xmlns:tika="http://namespaces.plone.org/tika">
            <tika:config path="${tika-app:destination}/${tika-app:filename}" />
        </configure>


Installing ftw.tika in Plone
----------------------------

- Install ``ftw.tika`` by adding it to the list of eggs in your buildout.
  (The buildout examples above include adding ``ftw.tika`` to the eggs).

.. code:: ini

    [instance]
    eggs +=
        ftw.tika

- Run buildout and start your instance

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

The path to the ``tika-app.jar`` file must be configured in ZCML.

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


Caching
-------

If you want the result of the transform to be cached, you'll need to pass a
persistent ZODB object to `transform_tool.convertTo()` to store the cached
result on.

For example, for a ``NamedBlobFile`` versioned with CMFEditions you'd
use ``namedfile.data`` to access the data of the current working copy, and
pass ``namedfile._blob`` as the object for the cache to be stored on (the
``namedfile`` is always the same instance for any version, only the ``_blob``
changes):

.. code:: python

            stream = transform_tool.convertTo(
                'text/plain',
                namedfile.data,
                mimetype=namedfile.contentType,
                object=namedfile._blob)


Stand-alone converter
---------------------

The code calling Tika is encapsulated in its own class, so if for some reason
you don't want to use the ``portal_transforms`` tool, you can also use the
converter directly by just instanciating it:

.. code:: python

            from ftw.tika.converter import TikaConverter

            data = StringIO('foo')
            converter = TikaConverter(path="/path/to/tika-app.jar")
            plain_text = converter.convert(data)

The ``convert()`` method accepts either a data string or a file-like stream
object. If no ``path`` keyword argument is supplied, the converter tries to
get the path to the ``tika-app.jar`` from the ZCML configuration.


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


.. _ftw-buildouts: https://github.com/4teamwork/ftw-buildouts#production
.. _tika.cfg: https://github.com/4teamwork/ftw.tika/blob/master/tika.cfg
