from setuptools import setup, find_packages
import os

version = '2.7.0'

tests_require = [
    'Products.CMFCore',
    'ftw.testing',
    'plone.app.testing',
    'plone.testing',
    'testfixtures',
    'unittest2',
    'zope.configuration',
    ]

setup(name='ftw.tika',
      version=version,
      description='Apache Tika integration for Plone using portal transforms.',
      long_description=open('README.rst').read() + '\n' +
      open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development',
        ],

      keywords='plone ftw tika full text indexing apache',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.tika',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'requests',

        # Zope
        'zope.component',
        'zope.interface',
        'zope.schema',
        'ZODB3',

        # Plone
        'Plone',
        'Products.GenericSetup',
        'Products.PortalTransforms',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
