# -*- encoding: utf-8 -*-

import logging

class BaseConfig(object):
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_VERSION = "0.0.0"     # Version number
    # adding version at the end of secret key to invalidate old tokens after new release
    SECRET_KEY = '\xea[\x88\xb9\xaa\x0e\x9c\xa7\xa9\x16\x06Za\xa9\x8d\x82e\xd0\xb0\r\x90%h@\x95 \xf3i\xc2\xdb-B'+APP_VERSION
    logger = logging.getLogger('digi-test')
    logger.setLevel(logging.INFO)


class DevelopmentConfig(BaseConfig):
    DEMO_MODE = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/digitiamo-development'
    logging.getLogger('digi-test').setLevel(logging.DEBUG)


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEMO_MODE = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/digitiamo-test'
    logging.getLogger('digi-test').setLevel(logging.DEBUG)
