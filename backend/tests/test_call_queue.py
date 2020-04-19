import time

import pytest

from backend.helpers import IPCache


@pytest.fixture
def ip_addresses():
    _ip_addresses = [
        "127.0.0.0",
        "127.0.0.1",
        "127.0.0.2",
        "127.0.0.3",
        "127.0.0.4"

    ]
    return _ip_addresses


@pytest.fixture
def test_ip_q():
    return IPCache(timeout=1, max_size=5)


@pytest.mark.usefixtures('app', 'test_ip_q', 'ip_addresses')
class TestApi:
    def test_insert_same_ip(self, test_ip_q):
        assert test_ip_q.put("127.0.0.2") is True
        # again but too early
        assert test_ip_q.put("127.0.0.2") is False
        time.sleep(2)
        # again but with timeout expired
        assert test_ip_q.put("127.0.0.2") is True

    def test_multiple_insert_ip(self, test_ip_q, ip_addresses):
        for ip in ip_addresses:
            assert test_ip_q.put(ip) is True
        assert test_ip_q.full() is True
        assert test_ip_q.put("127.0.0.5") is False
        time.sleep(2)
        assert test_ip_q.put("127.0.0.6") is True
        assert test_ip_q.full() is True
        time.sleep(2)
        for ip in ip_addresses:
            assert test_ip_q.put(ip) is True
        assert test_ip_q.put("127.0.0.6") is False

    def test_double_insert_ip(self, test_ip_q, ip_addresses):
        for ip in ip_addresses:
            assert test_ip_q.put(ip) is True
        assert test_ip_q.put("127.0.0.9") is False
        assert test_ip_q.full() is True
        assert test_ip_q.put("127.0.0.10") is False
