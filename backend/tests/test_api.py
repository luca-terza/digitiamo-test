import json
import os
from base64 import b64encode

import pytest
from ..models import User
from ..retiot.views import create_and_insert_client
from pprint import pprint


def _api_headers(client, db):
    create_single_user(db.session, "testApiClient", 'test.apiclient@test.com', "a test password",
                       "ApiClient")
    user = User.query.filter(User.username == 'testApiClient').first()

    post_valid_form(client, '/login', username='testApiClient', password='a test password')
    result = create_and_insert_client(data_for_oauth(user.id), user.id)
    assert isinstance(result, OAuth2Client)
    # assert b'client_secret' in result['client_info']
    data = {
        'grant_type': ['password'],
        'username': 'testApiClient',
        'password': 'a test password',
        'scope': 'dashboard database',
    }
    os.environ['AUTHLIB_INSECURE_TRANSPORT'] = "1"
    auth_token = str.encode("{}:{}".format(result.client_info['client_id'], result.client_info['client_secret']))

    headers = {
        'Authorization': f"Basic {b64encode(auth_token).decode('utf-8')}"
    }
    url = '/oauth/token'
    response = client.post(url, data=data, headers=headers, follow_redirects=True)
    assert response.status_code == 200, "POST %s returned %d" % (url, response.status_code)
    assert response_has_no_errors(response), "post_valid_form(%s) returned an error" % url
    oauth2_data = json.loads(response.data)
    r_access_token = oauth2_data['access_token']
    assert r_access_token is not None
    headers = {
        'Authorization': f"Bearer {r_access_token}"
    }
    os.environ['AUTHLIB_INSECURE_TRANSPORT'] = "1"

    return headers

class Mocked:
    def __init__(self, path):
        self.path = path

    def get(self):
        import os
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "snapshot.json"
        abs_file_path = os.path.join(script_dir, rel_path)

        mocked_file = open(abs_file_path, "r")
        return json.loads(mocked_file.read())


def mocked_fb_db(fake_path):
    return Mocked(fake_path)

@pytest.fixture
def headers(client, db):
    return _api_headers(client, db)


@pytest.mark.usefixtures('app', 'headers')
class TestApi:
    def _get_api(self, url, client, headers, code):
        response = client.get(url, headers=headers, follow_redirects=True)
        assert response.status_code == code, "GET %s returned %d" % (url, response.status_code)
        data = json.loads(response.data)
        return data

    def _post_api(self, url, client, headers, code):
        response = client.post(url, headers=headers, follow_redirects=True)
        assert response.status_code == code, "POST %s returned %d" % (url, response.status_code)
        data = json.loads(response.data)
        return data

    def test_nodelist(self, client, headers):
        url = '/api/v1.0/nodes_list'
        data = self._get_api(url, client, headers, 200)
        assert len(data['nodes']) > 0

    def test_visitors(self, client, headers):
        url = '/api/v1.0/visitors/all'
        data = self._get_api(url, client, headers, 200)
        assert len(data['data']) == 250
        url = '/api/v1.0/visitors/0'
        data = self._get_api(url, client, headers, 404)
        assert len(data['data']) == 0

    def test_mean_visitors(self, client, headers):
        # http://localhost:5000/api/v1.0/mean_visitors/all
        url = '/api/v1.0/mean_visitors/all'
        data = self._get_api(url, client, headers, 200)
        assert len(data) == 13
        assert data[0]['time_range'] == '0-30'

    def test_ages(self, client, headers):
        url = '/api/v1.0/ages/all'
        data = self._get_api(url, client, headers, 200)
        assert len(data) == 8
        assert data[0]['age_range'] == '10-16'

    def test_visitors_gender(self, client, headers):
        url = '/api/v1.0/visitors_gender/all'
        data = self._get_api(url, client, headers, 200)
        assert 'female' in data
        assert 'male' in data

    def test_punctual_visitors(self, client, headers):
        url = '/api/v1.0/punctual_visitors/all'
        data = self._get_api(url, client, headers, 200)
        assert len(data) > 0

    def test_visit_per_gender_and_age(self, client, headers):
        url = '/api/v1.0/visit-per-gender-and-age/all'
        data = self._get_api(url, client, headers, 200)
        assert 'columns' in data['data']

    def test_update_db(self, client, headers, mocker):

        mocker.patch('firebase_admin.db.reference', mocked_fb_db)
        url = '/api/v1.0/updateDb'
        data = self._post_api(url, client, headers, 200)
        assert data['message'] == 'db update completed'


