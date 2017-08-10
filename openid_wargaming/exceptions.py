"""Exceptions"""


class BadOpenIDReturnTo(Exception):
    def __init__(self, message, url):
        self.message = message
        self.url = url


class OpenIDFailReturnURLVerification(Exception):
    pass


class OpenIDVerificationFailed(Exception):
    def __init__(self, message, validator):
        self.message = message
        self.validator = validator
