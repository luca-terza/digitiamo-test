import requests, json
from flask_restful import Resource
from marshmallow import Schema, fields


class RequestIterator:
    """Class to implement an iterator
    while a redirect is returned"""

    def __init__(self, method, schema, request_url):
        self.http_method = getattr(requests, method.lower())
        self.schema = schema
        self.request_url = request_url
        # self.results = list()

    def __iter__(self):
        r = self.http_method(f"{self.schema}://{self.request_url}", allow_redirects=False)
        return self

    def __next__(self):
        if self.n <= self.max:
            result = 2 ** self.n
            self.n += 1
            return result
        else:
            raise StopIteration

# for h in r.history:
#     ...     print(h.headers['Server'])
# URL INFO
# Domain
# scheme
# path
#
# Response 0
# http/version status_code
# Location or Date
# Server/version

class MeanVisitorSchema(Schema):
    requested_url = fields.Url()
    headers = fields.Dict()
    server = fields.String()


class CallUrlRes(Resource):

    def get(self, method, schema, request_url):
        http_method = getattr(requests, method.lower())
        r = http_method(f"{schema}://{request_url}", allow_redirects=True)
        print(r.status_code, r.headers['Location'])
        return json.dumps(r.headers.__dict__['_store'])
        # r_log.info(f"to be implemented: {method} - {schema}://{request_url}")
