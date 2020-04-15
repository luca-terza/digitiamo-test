from datetime import datetime
from dateutil import tz

from backend import db, ma
# called_url
# schema
# method
# CONNECT
# DELETE
# GET
# HEAD
# OPTIONS
# PATCH
# POST
# PUT
# TRACE

class Call(db.Model):
    """ the mainn call with its schema, methods and url
    it is related to n results ( n > 1 when there are redirects)
    """
    __tablename__ = 'call'
    id = db.Column(db.Integer, primary_key=True)
    start_timestamp = db.Column(db.DateTime(), nullable=False)
    end_timestamp = db.Column(db.DateTime(), nullable=False)
    called_url = db.Column(db.String(256))
    request = db.Column(db.String(512))
    response = db.Column(db.CLOB())
    schema = db.Column(db.String(8))
    method = db.Column(db.String(16))


class CallResult(db.Model):
    """ results for each calls
    """
    __tablename__ = 'call_result'
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(
        db.Integer, db.ForeignKey('call.id'))
    call = db.relationship('Call')
    status = db.Column(db.Integer)
