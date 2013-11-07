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
  - ``*.docx`` Word Documents (``application/vnd.openxmlformats-officedocument.wordprocessingml.document``)
  - ``*.dotx`` Word Templates (``application/vnd.openxmlformats-officedocument.wordprocessingml.template``)
  - ``*.xlsx`` Excel Sheets (``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``)
  - ``*.xltx`` Excel Templates (``application/vnd.openxmlformats-officedocument.spreadsheetml.template``)
  - ``*.pptx`` Powerpoint Presentations (``application/vnd.openxmlformats-officedocument.presentationml.presentation``)
  - ``*.potx`` Powerpoint Templates (``application/vnd.openxmlformats-officedocument.presentationml.template``)
  - ``*.ppsx`` Powerpoint Slideshows (``application/vnd.openxmlformats-officedocument.presentationml.slideshow``)


Input formats supported by Tika, but not wired up yet
-----------------------------------------------------

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
file. Pass the path to the ``tika-app.jar`` to the converter when
instanciating it.


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


Usage
=====

To use ``ftw.tika``, simply instanciate the converter and pass it the path
to your ``tika-app.jar``:

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
