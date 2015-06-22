# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os

version = '2.3.dev0'
shortdesc = "Teaser/ Banner content type for Plone"
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += '\n' + open(
    os.path.join(
        os.path.dirname(__file__),
        'docs',
        'HISTORY.rst')
).read()


setup(name='collective.teaser',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Plone, Teaser, Banner',
      author='Johannes Raggam',
      author_email='raggam-nl@adm.at',
      url='http://github.com/collective/collective.teaser',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'archetypes.referencebrowserwidget',
          'node',
          'plone.api',
          'plone.app.portlets',
          'plone.formwidget.contenttree',
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
