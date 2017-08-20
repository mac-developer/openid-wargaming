"""Unit Test with pytest"""
from unittest import mock

import pytest

from openid_wargaming.authentication import Authentication


@pytest.fixture
@mock.patch('openid_wargaming.authentication.create_return_to')
def auth(mock_requests):
    mock_requests.return_value = 'http://somewhere'
    return Authentication()


@mock.patch('openid_wargaming.authentication.create_return_to')
def test_authentication_object(mock_requests, auth):
    mock_requests.return_value = 'http://somewhere'
    assert auth
    assert auth.mode == 'checkid_setup'
    assert auth.ns == 'http://specs.openid.net/auth/2.0'
    assert auth.identity == 'http://specs.openid.net/auth/2.0/' \
                            'identifier_select'
    assert auth.claimed_id == 'http://specs.openid.net/auth/2.0/' \
                              'identifier_select'
    assert auth.request_id
    assert auth.return_to


@mock.patch('openid_wargaming.authentication.get')
def test_authenticate(mock_requests, auth):
    from urllib.parse import urlparse

    endpoint = 'https://eu.wargaming.net/id/openid/'
    test_url = 'https://test.it/'
    headers = {'Location': test_url}
    mock_requests.return_value = mock.MagicMock(headers=headers)

    location = auth.authenticate(endpoint)
    parsed = urlparse(location)
    assert 'http' in location
    assert True if [parsed.scheme, parsed.netloc, parsed.path] else False


def test_fields_present_in_payload(auth):
    assert 'openid.mode' in auth.payload
    assert 'openid.ns' in auth.payload
    assert 'openid.identity' in auth.payload
    assert 'openid.claimed_id' in auth.payload
    assert 'openid.return_to' in auth.payload


def test_good_default_values_in_payload(auth):
    assert 'checkid_setup' == auth.payload['openid.mode']
    assert 'http://specs.openid.net/auth/2.0' == auth.payload['openid.ns']
    assert 'http://specs.openid.net/auth/2.0/' \
           'identifier_select' == auth.payload['openid.identity']
    assert 'http://specs.openid.net/auth/2.0/' \
           'identifier_select' == auth.payload['openid.claimed_id']
    assert auth.payload['openid.return_to']


def test_good_payload_conversion(auth):
    assert 'openid.ns=' in auth.convert(auth.payload)
    assert '&' in auth.convert(auth.payload)


def test_good_destination(auth):
    assert '?' in auth.destination(auth.convert(auth.payload))
    assert 'openid.ns=' in auth.destination(auth.convert(auth.payload))
    assert '&' in auth.destination(auth.convert(auth.payload))


def test_evidence_is_good(auth):
    from datetime import datetime
    assert isinstance(auth.evidence['timestamp'], datetime)
    assert 'request_id' in auth.evidence
