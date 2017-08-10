"""Some general utilities"""
from requests import post


REQUESTBIN='https://requestb.in/api/v1/bins'


def create_return_to(request_id):
    """Create a return url to do tests and analyze information

    This function prevents you from create a website for testing.
    It allows you to develop quickly.

    Reference: requestb.in
    Alternatives: httpbin.org
    """
    r = post(REQUESTBIN, {"private": "false"})
    bin = r.json()['name']
    url = 'https://requestb.in/%s?request_id=%s' % (bin, request_id)
    return url


def nonce_saver(payload):
    return True


def nonce_reader(nonce):
    return False
