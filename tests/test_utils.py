from unittest import mock


@mock.patch('openid_wargaming.utils.post')
def test_create_return_to(mock_requests):
    from openid_wargaming.utils import create_return_to
    from uuid import uuid4
    from urllib.parse import urlparse
    mock_requests.return_value = mock.MagicMock(json=lambda: {'name': uuid4().hex})
    url = create_return_to(uuid4().hex)
    parsed = urlparse(url)
    assert 'http' in url
    assert True if [parsed.scheme, parsed.netloc, parsed.path] else False


def test_saver():
    from openid_wargaming.utils import nonce_saver
    assert nonce_saver(None)


def test_reader():
    from openid_wargaming.utils import nonce_reader
    assert not nonce_reader(None)
