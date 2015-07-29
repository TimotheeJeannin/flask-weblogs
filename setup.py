# coding=utf-8
"""
Flask-WebLogs
-------------

Monitor logs from the web.
"""
from setuptools import setup

setup(
    name='Flask-WebLogs',
    version='1.0',
    license='MIT',
    author='Timothée Jeannin',
    author_email='timojeajea@gmail.com',
    maintainer='Timothée Jeannin',
    maintainer_email='timojeajea@gmail.com',
    include_package_data=True,
    packages=[
        'flask_weblogs'
    ],
    install_requires=[
        'Flask==0.10',
        'gevent==1.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
