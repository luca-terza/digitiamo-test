import json
import os
from base64 import b64encode

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


@pytest.mark.usefixtures('app', 'client')
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

    def test_get_call(self, client):
        url = '/api/v1.0/request_url/GET?query={ "requested_url": "http://www.instagram.com"} '
        data = self._get_api(url, client, 200)
        assert len(data) > 0
