# -*- encoding: utf-8 -*-

import logging


class BaseConfig(object):
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_VERSION = "0.1.0"     # Version number
    # adding version at the end of secret key to invalidate old tokens after new release
    SECRET_KEY = 'T\xc4<\xd1\xdf\xf5*7<u>=\xa0\x9f\x8e\xe7>\x81O\x18I\x02\x90\x89'+APP_VERSION
    logger = logging.getLogger('digi-test')
    logger.setLevel(logging.INFO)


class DevelopmentConfig(BaseConfig):
    DEMO_MODE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///digitiamo-development.sqlite3'
    logging.getLogger('digi-test').setLevel(logging.DEBUG)


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEMO_MODE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///digitiamo-test.sqlite3'
    logging.getLogger('digi-test').setLevel(logging.DEBUG)
