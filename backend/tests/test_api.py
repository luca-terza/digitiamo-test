import json
import random
import flask
from pprint import pprint
import pytest


def mocked_remote_addr():
    return f"127.0.0.{random.randint(1, 5000)}"


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


    def _call_url(self, method, query, client, asserted_staus_code):
        url = f'/api/v1.0/request_url/{method}?query={query} '
        data = self._get_api(url, client, asserted_staus_code)
        print('\n-------------')
        pprint(data)
        assert len(data) > 0

    def test_get_call(self, client, queries, mocker):
        mocker.patch.object(flask.Request, 'remote_addr', mocked_remote_addr)

        print('\n***************************************')
        for q in queries:
            self._call_url('GET', json.dumps(q), client, 200)

    def test_get_call_failure(self, client, queries, ):
        print('\n***************************************')
        #first is ok
        self._call_url('GET', json.dumps({"requested_url": "https://duckduckgo.com"}), client, 200)
        #next are from the same remote address within the timeout
        for q in queries:
            self._call_url('GET', json.dumps(q), client, 404)

    def test_post_call(self, client, queries, mocker):
        mocker.patch.object(flask.Request, 'remote_addr', mocked_remote_addr)
        print('\n***************************************')
        self._call_url('POST', json.dumps({"requested_url": "http://www.instagram.com"}), client, 200)
        self._call_url('POST', json.dumps({"requested_url": "http://www.google.com"}), client, 405)
