# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from backend import create_app, db as _db


@pytest.fixture(scope='session', autouse=True)
def app():
    """Create application for the tests."""
    _app = create_app("Testing")

    yield _app


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()
    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()

