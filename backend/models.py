from datetime import datetime
from dateutil import tz

from backend import db, ma
from sqlalchemy.dialects.postgresql.json import JSONB

class Visitor(db.Model):
    """ the people detected by the node

    store information about visitor's as personal data, emotion

    face_info are stored as JSON to allow maximum flexibility
        https://www.postgresql.org/docs/current/datatype-json.html

    """
    __tablename__ = 'visitors'
    id = db.Column(db.Integer, primary_key=True)
    visit_timestamp = db.Column(db.DateTime(), nullable=False, index=True)
    duration = db.Column(db.Integer(), index=True)
    face_id = db.Column(db.String(256))
    node_tz = db.Column(db.String(256))
    average_distance = db.Column(db.Float)
    minimum_distance = db.Column(db.Float)
    visitor_id = db.Column(db.String)
    age = db.Column(db.Float, nullable=True, index=True)
    gender = db.Column(db.String, nullable=True, index=True)
    num_of_visits = db.Column(db.Integer, default=1)
    node_id = db.Column(db.Integer(), db.ForeignKey('nodes.id'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    face_info = db.Column(JSONB())

    def __init__(self, visit_timestamp, duration, average_distance, minimum_distance,
                 visitor_id=None, age=None, gender=None):
        ts_info = convert_timestamp(visit_timestamp)
        self.visit_timestamp = ts_info['utc_timestamp']
        self.node_tz = ts_info['tz_offset']
        # TODO self.returning_visitor
        self.duration = duration
        self.average_distance = average_distance
        self.minimum_distance = minimum_distance
        self.visitor_id = visitor_id or None
        self.age = age or None
        self.gender = gender or 'unknown'
