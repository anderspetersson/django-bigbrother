#!/usr/bin/env python
from setuptools import setup,find_packages

METADATA = dict(
    name='django-bigbrother',
    version='0.1.0',
    author='Anders Petersson',
    author_email='me@anderspetersson.se',
    description='Modular Dashboard for Django Projects',
    long_description=open('README.md').read(),
    url='http://github.com/anderspetersson/django-bigbrother',
    keywords='django dashboard bigbrother monitoring',
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers, Sysadmins',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe = False,
    packages=find_packages(),
    package_data={'bigbrother': ['templates/bigbrother/*.html', 'static/*'], }
)

if __name__ == '__main__':
    setup(**METADATA)
