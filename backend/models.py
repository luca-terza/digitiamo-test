from marshmallow import Schema, fields
from backend import db, ma
from sqlalchemy.orm import relationship

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
    status_code = fields.Int()
    location = fields.String(required=False)
    date = fields.String(required=False)
    # date = fields.Date(required=False, dateformat="%d/%m/%Y")
    server = fields.String(required=False)


class CallSchema(Schema):
    share_id = fields.Int()
    requested_url = fields.Url()
    domain = fields.String()
    scheme = fields.String()
    method = fields.String()
    path = fields.String()
    call_results = fields.List(fields.Nested(CallResultSchema))


class Call(db.Model):
    """ the main call with its schema, methods and url
    it is related to n results ( n > 1 when there are redirects)
    """
    __tablename__ = 'call'
    id = db.Column(db.Integer, primary_key=True)
    start_timestamp = db.Column(db.DateTime(), nullable=False)
    end_timestamp = db.Column(db.DateTime(), nullable=False)
    requested_url = db.Column(db.String(256))
    domain = db.Column(db.String(256))
    scheme = db.Column(db.String(16))
    method = db.Column(db.String(16))
    path = fields.String()
    call_results = relationship("CallResult", backref="call")


class CallResult(db.Model):
    """ results for each calls
    """
    __tablename__ = 'call_result'
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(
        db.Integer, db.ForeignKey('call.id'))
    status_code = db.Column(db.Integer())
    location = db.String(db.String(256))
    server = db.String(db.String(256))
    date = db.Column(db.DateTime())
