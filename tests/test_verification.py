from unittest import mock

import pytest

from openid_wargaming.verification import Verification


@pytest.fixture
def verify():
    assertion_url = 'https://somewhere.com/?openid.return' \
                    '_to=http://another.url&' \
                    'openid.identity=JohnDoe&openid.claimed_id=JohnDoe'
    return Verification(assertion_url)


def test_verification_object(verify):
    from openid_wargaming.utils import nonce_saver
    from openid_wargaming.utils import nonce_reader
    assert verify
    assert verify.saver == nonce_saver
    assert verify.reader == nonce_reader


def test_return_to_is_present_on_assertion_url(verify):
    assert 'http'in verify.return_to
    assert True if [verify.return_to.scheme,
                    verify.return_to.netloc,
                    verify.return_to.path] else False


def test_return_to_is_not_present_on_assertion_url(verify):
    assertion_url = 'https://somewhere.com/?some_kind_of_error=True'
    verify = Verification(assertion_url)
    assert verify.return_to is None


def test_is_positive_assertion_fail_with_exception():
    from openid_wargaming.exceptions import BadOpenIDReturnTo
    assertion_url = 'https://somewhere.com/?some_kind_of_info'
    verify = Verification(assertion_url)
    with pytest.raises(BadOpenIDReturnTo):
        verify.is_positive_assertion()


def test_is_positive_assertion_fail_with_openid_error():
    assertion_url = 'https://somewhere.com/?openid.mode=cancel'
    verify = Verification(assertion_url)
    assert not verify.is_positive_assertion()


def test_is_positive_assertion_success():
    assertion_url = 'https://somewhere.com/?openid.mode=id_res'
    verify = Verification(assertion_url)
    assert verify.is_positive_assertion()


def test_return_url_base_params_not_present_on_the_current_url():
    from openid_wargaming.exceptions import OpenIDFailReturnURLVerification
    assertion_url = 'https://somewhere.com/?openid.mode=id_res&openid.' \
                    'return_to=https://somewhere'
    verify = Verification(assertion_url)

    with pytest.raises(OpenIDFailReturnURLVerification):
        verify.verify_return_url()


def test_return_url_query_params_not_present_on_the_current_url():
    from openid_wargaming.exceptions import OpenIDFailReturnURLVerification
    assertion_url = 'https://somewhere.com/?openid.mode=id_res&openid.' \
                    'return_to=https://somewhere.com/?request_id=ID1&'
    verify = Verification(assertion_url)

    with pytest.raises(OpenIDFailReturnURLVerification):
        verify.verify_return_url()


def test_return_url_query_params_present_on_the_current_url_and_with_same_value():
    from openid_wargaming.exceptions import OpenIDFailReturnURLVerification
    assertion_url = 'https://somewhere.com/?openid.mode=id_res&openid.' \
                    'return_to=https%3A%2F%2Fsomewhere.com%2F%3Frequest_id%3DID1&request_id=ID1'
    verify = Verification(assertion_url)

    # with pytest.raises(OpenIDFailReturnURLVerification):
    assert verify.verify_return_url()


def test_return_url_query_params_present_on_the_current_url_and_with_different_value():
    from openid_wargaming.exceptions import OpenIDFailReturnURLVerification
    assertion_url = 'https://somewhere.com/?openid.mode=id_res&openid.' \
                    'return_to=https%3A%2F%2Fsomewhere.com%2F%3Frequest_id%3DID1&request_id=ID2'
    verify = Verification(assertion_url)

    with pytest.raises(OpenIDFailReturnURLVerification):
        verify.verify_return_url()


def test_verify_discovered_information(verify):
    assert verify.verify_discovered_information()


def test_check_nonce():
    assertion_url = 'https://somewhere.com/?openid.mode=id_res&openid.' \
                    'return_to=https%3A%2F%2Fsomewhere.com%2F%3Frequest_id' \
                    '%3DID1&request_id=ID2&openid.response_nonce=somevalue'
    verify = Verification(assertion_url)

    assert verify.check_nonce()


@mock.patch('openid_wargaming.verification.nonce_reader')
def test_check_nonce_failed(mock_request):
    assertion_url = 'https://somewhere.com/?openid.mode=id_res&openid.' \
                    'return_to=https%3A%2F%2Fsomewhere.com%2F%3Frequest_id' \
                    '%3DID1&request_id=ID2&openid.response_nonce=somevalue'

    mock_request.return_value = True
    verify = Verification(assertion_url)
    assert not verify.check_nonce()


@mock.patch('openid_wargaming.verification.post')
def test_verify_signatures_success(mock_request):
    return_value = """
    is_valid: true
    field1: value1
    """
    mock_request.return_value.text = return_value
    assertion_url = 'https://somewhere.com/?openid.mode=check_authentication' \
                    '&openid.' \
                    'return_to=https%3A%2F%2Fsomewhere.com%2F%3Frequest_id' \
                    '%3DID1&request_id=ID2&openid.response_nonce=somevalue&' \
                    'openid.op_endpoint=http://somewhere.com'
    verify = Verification(assertion_url)

    assert verify.verify_signatures()


@mock.patch('openid_wargaming.verification.post')
def test_verify_signatures_failed(mock_request):
    return_value = """
    is_valid: false
    field1: value1
    """
    mock_request.return_value.text = return_value
    assertion_url = 'https://somewhere.com/?openid.mode=check_authentication' \
                    '&openid.' \
                    'return_to=https%3A%2F%2Fsomewhere.com%2F%3Frequest_id' \
                    '%3DID1&request_id=ID2&openid.response_nonce=somevalue&' \
                    'openid.op_endpoint=http://somewhere.com'
    verify = Verification(assertion_url)

    assert not verify.verify_signatures()


def test_fields_presence_in_identity(verify):
    assert 'identity' in verify.identify_the_end_user()
    assert 'claimed_id' in verify.identify_the_end_user()


def test_verify_failed():
    from openid_wargaming.exceptions import OpenIDVerificationFailed
    assertion_url = 'https://somewhere.com/?openid.mode=check_authentication' \
                    '&openid.' \
                    'return_to=https%3A%2F%2Fsomewhere.com%2F%3Frequest_id' \
                    '%3DID1&request_id=ID2&openid.response_nonce=somevalue&' \
                    'openid.op_endpoint=http://somewhere.com'
    verify = Verification(assertion_url)

    with pytest.raises(OpenIDVerificationFailed):
        verify.verify()


@mock.patch('openid_wargaming.verification.post')
def test_verify_success(mock_request):
    return_value = """
    is_valid: true
    field1: value1
    """
    mock_request.return_value.text = return_value
    assertion_url = 'https://somewhere.com/?openid.mode=id_res' \
                    '&openid.' \
                    'return_to=https%3A%2F%2Fsomewhere.com%2F%3Frequest_id' \
                    '%3DID1&request_id=ID1&openid.response_nonce=somevalue&' \
                    'openid.op_endpoint=http://somewhere.com&' \
                    'openid.identity=JohnDoe&openid.claimed_id=JohnDoe'
    verify = Verification(assertion_url)
    verify.verify()
