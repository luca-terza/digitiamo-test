import json
from urllib.parse import urlparse

import requests
from flask import request
from flask_restful import Resource

from backend.models import Call, CallResult


def safe_param(d, key):
    try:
        return d[key]
    except KeyError:
        return None


class CallUrlRes(Resource):

    def _set_call_result(self, h):
        CallResult(status_code=h.status_code,
                   location=safe_param(h.headers, 'location'),
                   date=safe_param(h.headers, 'date'),
                   server=safe_param(h.headers, 'server')
                   )

    def get(self, method):
        json_query = request.args
        requested_url = json.loads(json_query['query'])['requested_url']
        http_method = getattr(requests, method.lower())
        parsed_url = urlparse(requested_url)
        call = Call(domain=parsed_url.netloc,
                    scheme=parsed_url.scheme,
                    method=method,
                    path=parsed_url.path)
        r = http_method(f"{requested_url}", allow_redirects=True)
        for h in r.history:
            call.call_results.append(self._set_call_result(h))
        call.call_results.append(self._set_call_result(r))
        return json.dumps(r.headers.__dict__['_store'])
