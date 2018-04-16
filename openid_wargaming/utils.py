"""Some general utilities"""
from uuid import uuid4
from requests import get


HTTPBIN='https://httpbin.org/get'


def create_return_to(request_id):
    """Create a return url to do tests and analyze information

    This function prevents you from create a website for testing.
    It allows you to develop quickly.

    Reference: httpbin.org
    """
    r = get(HTTPBIN, {"uuid": uuid4().hex})
    url = r.json()['url']
    return url


def nonce_saver(payload):
    return True


def nonce_reader(nonce):
    return False
