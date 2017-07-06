#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='TorAliMNS',
    version='0.0.1',
    author='Sihao Zhang',
    author_email='zhangsihao@1zhen.com',
    packages=['toralimns'],
    description='Tornado aliyun mns client',
    scripts = ["bin/tormnscmd"],
    install_requires=[
        'tornado'
    ],
    include_package_data=True
)