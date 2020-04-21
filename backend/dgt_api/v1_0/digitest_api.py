import json
import random
import requests
import re
from urllib.parse import urlparse
from flask import request
from flask_restful import Resource
from hyper.contrib import HTTP20Adapter
from hyper.http11.response import HTTP11Response
from requests.cookies import extract_cookies_to_jar
from requests.models import Response
from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers

from backend import db, ip_cache
from backend.models import Call, CallResult, CallSchema


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
                try:
                    new_item.append(i.decode())
                except AttributeError:
                    print("error")
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
        return ''


def safe_decode(s_or_b):
    try:
        return s_or_b.decode()
    except AttributeError:
        return s_or_b


def get_last_date(h):
    try:
        return re.split("GMT, ", h['date'])[-1]
    except KeyError:
        return ''


class CallUrlRes(Resource):
    def _create_random_handle(self):
        return str(hex(random.randint(10000000, 90000000)))[2:]

    def _set_call_result(self, h):
        protocol = 'HTTP/'

        if type(h.raw) == HTTP11Response:
            protocol += '1.1'
        else:
            protocol += '2'

        return CallResult(status_code=f"{protocol} {h.status_code} {safe_decode(h.reason)}",
                          location=safe_param(h.headers, 'location'),
                          date=get_last_date(h.headers),
                          server=safe_param(h.headers, 'server')
                          )

    def _status_from_ex(self, e):
        ex_dict = {requests.exceptions.MissingSchema: 406, 'default': 404}
        try:
            return ex_dict[type(e)]
        except KeyError:
            return ex_dict['default']

    def _handle_request(self, method, requested_url):
        if not ip_cache.put(request.remote_addr):
            return {'error': 'address not allowed'}, 404

        parsed_url = urlparse(requested_url)

        call = Call(domain=parsed_url.netloc,
                    scheme=parsed_url.scheme,
                    method=method,
                    path=(parsed_url.path or '/'),
                    requested_url=requested_url,
                    errors='')
        s = requests.Session()
        s.mount(requested_url, MyHTTP20Adapter())
        http_method = getattr(s, method.lower())
        r = None
        try:
            r = http_method(f"{requested_url}", allow_redirects=True)
            for h in r.history:
                call.call_results.append(self._set_call_result(h))
            call.call_results.append(self._set_call_result(r))
            call.status = r.status_code
        except Exception as e:
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = e
            call.errors += f"'error': '{msg}'"
            call.status = self._status_from_ex(e)
        db.session.add(call)
        db.session.commit()
        call.handle = f"{self._create_random_handle()}{call.id}"
        db.session.add(call)
        db.session.commit()
        schema = CallSchema()
        return {'result': schema.dump(call)}, call.status

    def get(self, method):
        json_query = request.args
        requested_url = json.loads(json_query['query'])['requested_url']
        return self._handle_request(method, requested_url)

    def post(self, method):
        requested_url = json.loads(request.data.decode())['requested_url']
        return self._handle_request(method, requested_url)
