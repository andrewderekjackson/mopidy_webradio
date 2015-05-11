# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging
import os
import mopidy_test

import pygst

pygst.require('0.10')
import gst
import gobject

from mopidy import config, exceptions, ext
__author__ = 'Andrew Jackson'
__email__ = 'andrewderekjackson@gmail.com'
__version__ = '0.1.0'


# If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)

class Extension(ext.Extension):

    dist_name = 'Mopidy-Test'
    ext_name = 'test'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['username'] = config.String()
        schema['password'] = config.Secret()
        return schema

    def get_command(self):
        pass

    def validate_environment(self):
        pass

    def setup(self, registry):

        # Register a frontend
        from .mopidy_test import TestFrontend
        registry.add('frontend', TestFrontend)

        pass