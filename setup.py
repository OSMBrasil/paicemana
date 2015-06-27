from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='paicemana',
      version='0.0.1',
      description="Helper script for works at OSMBrasil/semanario",
      long_description=long_description,
      classifiers=[],
      keywords=['openstreetmap', 'osm', 'translations', 'weeklyosm'],
      author="Alexandre Magno",
      author_email='alexandre.mbm@gmail.com',
      url='https://github.com/OSMBrasil/paicemana',
      license='GPLv3+',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'html2text',
          'lxml'
      ],
      entry_points="""
      [console_scripts]
      paicemana=paicemana.scripts.cli:cli
      """
      )
