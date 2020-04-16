from flask import redirect, request
from flask_restful import Resource, abort
from marshmallow import Schema, fields, validates, ValidationError
from backend import r_log
import requests


class CallUrlRes(Resource):

    def get(self, method, schema, request_url):
        http_method = getattr(requests, method.lower())
        result = http_method(f"{schema}://{request_url}")
        return result
        # r_log.info(f"to be implemented: {method} - {schema}://{request_url}")
