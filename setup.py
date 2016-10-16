from distutils.core import setup
from setuptools import find_packages

REQUIREMENTS = [
    'marvinbot'
]

setup(name='marvinbot-urban-dictionary-plugin',
      version='0.1',
      description='Urban Dictionary plugin for marvinbot',
      author='Ricardo Cabral',
      author_email='ricardo.arturo.cabral@gmail.com',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      package_data={'': ['*.ini']},
      install_requires=REQUIREMENTS,
      dependency_links=[
          'git+ssh://git@github.com:BotDevGroup/marvin.git#egg=marvinbot',
      ],)
