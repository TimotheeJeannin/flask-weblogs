# coding=utf-8
"""
Flask-WebLogs
-------------

Monitor logs from the web.
"""
from setuptools import setup, find_packages


def get_requirements(suffix=''):
    with open('requirements%s.txt' % suffix) as f:
        rv = f.read().splitlines()
    return rv


setup(
    name='Flask-WebLogs',
    version='1.0',
    license='MIT',
    author='Timothée Jeannin',
    author_email='timojeajea@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
