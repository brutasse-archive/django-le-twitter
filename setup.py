# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages


setup(
    name='django-le-twitter',
    version='0.1',
    author=u'Bruno Renie',
    author_email='bruno@renie.fr',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/brutasse/django-le-twitter',
    license='BSD licence, see LICENCE file',
    description='Twitter authentication that sucks',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django>=1.3',
        #'tweepy>=1.5',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
