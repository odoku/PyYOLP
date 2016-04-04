# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='PyYOLP',
    version='0.0.1',
    description='Yahoo! Open Local Platform(YOLP) client for python.',
    author='odoku',
    author_email='masashi.onogawa@wamw.jp',
    keywords='yolp,yahoo',
    url='http://github.com/odoku/PyYOLP',

    packages=['yolp'],
    install_requires=[
        'requests>=2.9.1',
        'xmltodict>=0.10.1',
    ],
    extras_require={
        'test': ['pytest==2.9.1'],
    }
)
