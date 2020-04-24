import json
import random
import requests
import re
from urllib.parse import urlparse
from flask import request
from flask_restful import Resource
from hyper.http11.response import HTTP11Response
from backend.hyper_monkey_patch import MyHTTP20Adapter
from backend import db, ip_cache
from backend.models import Call, CallResult, CallSchema
from http import HTTPStatus


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

        return CallResult(status_code=f"{protocol} {h.status_code} {self._get_status_name(h.status_code)}",
                          location=safe_param(h.headers, 'location'),
                          date=get_last_date(h.headers),
                          server=safe_param(h.headers, 'server')
                          )

    def _status_from_ex(self, e):
        ex_dict = {requests.exceptions.MissingSchema: 406, 'default': 501}
        try:
            return ex_dict[type(e)]
        except KeyError:
            return ex_dict['default']

    def _get_reason(self, status):
        return HTTPStatus(status).description

    def _get_status_name(self, status):
        return HTTPStatus(status).name.replace('_', ' ')

    def _sanitize_url(self, url):
        p = re.compile("(http|https):\/\/")
        if not p.search(url):
            url = "http://"+url
        return url

    def _handle_request(self, method, requested_url):
        if not ip_cache.put(request.remote_addr):
            return {'error': 'address not allowed'}, 404

        requested_url = self._sanitize_url(requested_url)

        parsed_url = urlparse(requested_url)
        call = Call(domain=parsed_url.netloc,
                    scheme=parsed_url.scheme,
                    method=method,
                    path=(parsed_url.path or '/'),
                    requested_url=requested_url,
                    errors='')
        s = requests.Session()
        s.mount(requested_url, MyHTTP20Adapter())
        try:
            http_method = getattr(s, method.lower())
            r = http_method(f"{requested_url}", allow_redirects=True)
            for h in r.history:
                call.call_results.append(self._set_call_result(h))
            call.call_results.append(self._set_call_result(r))
            call.status = r.status_code
            call.status_msg = self._get_reason(r.status_code)
        except Exception as e:
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = e
            call.errors += f'{{"error": "{msg}" }}'
            call.status = 501
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


class ShareRes(Resource):
    def get(self, share_id):
        call = Call.query.filter_by(handle=share_id).first()
        if call:
            schema = CallSchema()
            return {'result': schema.dump(call)}
        else:
            return {'result': {}}, 404
