import json
from urllib.parse import urlparse

import requests
from flask import request
from flask_restful import Resource

from backend.models import Call, CallResult, CallSchema
from hyper.contrib import HTTP20Adapter
from requests.models import Response
from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers
from requests.cookies import extract_cookies_to_jar

class MyHTTP20Adapter(HTTP20Adapter):
    def _my_iter_raw(self, items):
        """
        Allows iterating over the headers in 'raw' form: that is, the form in
        which they were added to the structure. This iteration is in order,
        and can be used to rebuild the original headers (e.g. to determine
        exactly what a server sent).
        """
        for item in items:
            new_item = list()
            for i in item:
                new_item.append(i.decode())
            yield tuple(new_item)

    def build_response(self, request, resp):
        """
        Builds a Requests' response object.  This emulates most of the logic of
        the standard fuction but deals with the lack of the ``.headers``
        property on the HTTP20Response object.

        Additionally, this function builds in a number of features that are
        purely for HTTPie. This is to allow maximum compatibility with what
        urllib3 does, so that HTTPie doesn't fall over when it uses us.
        """
        response = Response()

        response.status_code = resp.status
        response.headers = CaseInsensitiveDict(self._my_iter_raw(resp.headers))
        response.raw = resp
        response.reason = resp.reason
        response.encoding = get_encoding_from_headers(response.headers)

        extract_cookies_to_jar(response.cookies, request, response)
        response.url = request.url

        response.request = request
        response.connection = self

        # First horrible patch: Requests expects its raw responses to have a
        # release_conn method, which I don't. We should monkeypatch a no-op on.
        resp.release_conn = lambda: None

        # Next, add the things HTTPie needs. It needs the following things:
        #
        # - The `raw` object has a property called `_original_response` that is
        #   a `httplib` response object.
        # - `raw._original_response` has three simple properties: `version`,
        #   `status`, `reason`.
        # - `raw._original_response.version` has one of three values: `9`,
        #   `10`, `11`.
        # - `raw._original_response.msg` exists.
        # - `raw._original_response.msg._headers` exists and is an iterable of
        #   two-tuples.
        #
        # We fake this out. Most of this exists on our response object already,
        # and the rest can be faked.
        #
        # All of this exists for httpie, which I don't have any tests for,
        # so I'm not going to bother adding test coverage for it.
        class FakeOriginalResponse(object):  # pragma: no cover
            def __init__(self, headers):
                self._headers = headers

            def get_all(self, name, default=None):
                values = []

                for n, v in self._headers:
                    if n == name.lower():
                        values.append(v)

                if not values:
                    return default

                return values

            def getheaders(self, name):
                return self.get_all(name, [])

        response.raw._original_response = orig = FakeOriginalResponse(None)
        orig.version = 20
        orig.status = resp.status
        orig.reason = resp.reason
        orig.msg = FakeOriginalResponse(resp.headers.iter_raw())

        return response

def safe_param(d, key):
    try:
        return d[key]
    except KeyError:
        return None


def get_last_date(h):
    try:
        return h.raw.headers._container['date'][len(h.raw.headers._container['date']) - 1]
    except KeyError:
        return None


class CallUrlRes(Resource):

    def _set_call_result(self, h):
        return CallResult(status_code=h.status_code,
                          location=safe_param(h.headers, 'location'),
                          date='test',
                          server=safe_param(h.headers, 'server')
                          )

    def get(self, method):
        json_query = request.args
        requested_url = json.loads(json_query['query'])['requested_url']
        parsed_url = urlparse(requested_url)
        call = Call(domain=parsed_url.netloc,
                    scheme=parsed_url.scheme,
                    method=method,
                    path=parsed_url.path)
        s = requests.Session()
        s.mount(requested_url, MyHTTP20Adapter())
        http_method = getattr(s, method.lower())
        r = http_method(f"{requested_url}", allow_redirects=True)
        for h in r.history:
            call.call_results.append(self._set_call_result(h))
        call.call_results.append(self._set_call_result(r))
        schema = CallSchema()
        return {'result': schema.dump(call)}, r.status_code
