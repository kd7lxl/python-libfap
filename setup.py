#!/usr/bin/env python

from distutils.core import setup
setup(name='python-libfap',
        version='0.1',
        description='Python ctypes bindings for libfap, the C port of the HAM::APRS::FAP Finnish APRS Parser',
        author='Tom Hayward',
        author_email='tom@tomh.us',
        url='https://github.com/kd7lxl/python-libfap',
        py_modules=['libfap'],
        )

