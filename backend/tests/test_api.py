import json
import os
from base64 import b64encode
from pprint import pprint

import pytest


class Mocked:
    def __init__(self, path):
        self.path = path

    def get(self):
        import os
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "snapshot.json"
        abs_file_path = os.path.join(script_dir, rel_path)

        mocked_file = open(abs_file_path, "r")
        return json.loads(mocked_file.read())


def mocked_fb_db(fake_path):
    return Mocked(fake_path)


@pytest.fixture
def queries():
    _queries = [
        {"requested_url": "http://www.instagram.com"},
        {"requested_url": "http://www.google.com"},
        {"requested_url": "https://www.instagram.com"},
        {"requested_url": "https://google.com"},
        {"requested_url": "https://python.org"},
        {"requested_url": "https://www.google.com"},

    ]
    return _queries


@pytest.mark.usefixtures('app', 'client', 'queries')
class TestApi:
    def _call_api(self, schema, method, request_url, client, code):
        # http_method = getattr(client, method)
        url = '/api/v1.0/request_url'
        response = client.get(url, schema, method, request_url, follow_redirects=True)
        assert response.status_code == code, f" {method} %s returned %d" % (url, response.status_code)
        data = json.loads(response.data)
        return data

    def _get_api(self, url, client, code):
        response = client.get(url, follow_redirects=True)
        assert response.status_code == code, "GET %s returned %d" % (url, response.status_code)
        data = json.loads(response.data)
        return data

    def _post_api(self, url, client, code):
        response = client.post(url, follow_redirects=True)
        assert response.status_code == code, "POST %s returned %d" % (url, response.status_code)
        data = json.loads(response.data)
        return data


    def _call_url(self, method, query, client):
        url = f'/api/v1.0/request_url/{method}?query={query} '
        data = self._get_api(url, client, 200)
        print('\n-------------')
        pprint(data)
        assert len(data) > 0

    def test_get_call(self, client, queries):
        print('\n***************************************')
        for q in queries:
            self._call_url('GET', json.dumps(q), client)

    def test_head_call(self, client, queries):
        print('\n***************************************')
        for q in queries:
            self._call_url('HEAD', json.dumps(q), client)
