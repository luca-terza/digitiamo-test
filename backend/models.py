from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy.orm import relationship

from backend import db


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


class CallResultSchema(Schema):
    status_code = fields.String()
    location = fields.String(required=False)
    date = fields.String(required=False)
    server = fields.String(required=False)


class CallSchema(Schema):
    share_id = fields.String(attribute="handle")
    requested_url = fields.Url()
    domain = fields.String()
    schema = fields.String(attribute="scheme")
    method = fields.String()
    path = fields.String()
    status = fields.Int()
    status_msg = fields.String()
    errors = fields.String()
    date = fields.Date(attribute="created_on", format="%a, %e %b %Y")
    call_results = fields.List(fields.Nested(CallResultSchema))


class Call(db.Model):
    """ the main call with its schema, methods and url
    it is related to n results ( n > 1 when there are redirects)
    """
    __tablename__ = 'call'
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(256), unique=True, index=True)
    requested_url = db.Column(db.String(256))
    domain = db.Column(db.String(256))
    scheme = db.Column(db.String(16))
    method = db.Column(db.String(16))
    path = db.Column(db.String(256))
    call_results = relationship("CallResult", backref="call")
    status = db.Column(db.Integer)
    status_msg = db.Column(db.String(256))
    errors = db.Column(db.String(1024))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)


class CallResult(db.Model):
    """ results for each calls
    """
    __tablename__ = 'call_result'
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(
        db.Integer, db.ForeignKey('call.id'))
    status_code = db.Column(db.String(256))
    location = db.Column(db.String(256))
    server = db.Column(db.String(256))
    date = db.Column(db.String(256))
