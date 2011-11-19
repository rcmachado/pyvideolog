import httplib

import unittest2
import fudge
from fudge.inspector import arg

from videolog.core import APIError, Videolog
from tests.unit.testcase import BaseTestCase

class VideologTestCase(BaseTestCase):
    def setUp(self):
        fudge.clear_calls()
        fudge.clear_expectations()

    def tearDown(self):
        fudge.verify()

    @fudge.patch('httplib.HTTPConnection')
    def test_can_login(self, HTTPConnection):
        headers = {
            'Token': '0123my_token',
            'Content-type': 'application/x-www-form-urlencoded',
        }
        self.httpconnection_mock(HTTPConnection, 'POST', '<api_url>',
                                 '/usuario/login', arg.any(),
                                 headers, "Autenticacao=HASHAUTENTICACAO")


        api = Videolog("<api_url>", "0123my_token")
        self.assertTrue(api.login("<login>", "<senha>"))

    @fudge.patch('httplib.HTTPConnection')
    def test_can_not_login_with_invalid_user(self, HTTPConnection):
        headers = {
            'Token': '0123my_token',
            'Content-type': 'application/x-www-form-urlencoded',
        }

        self.httpconnection_mock(HTTPConnection, 'POST', '<api_url>',
                                 '/usuario/login', arg.any(),
                                 headers, "LOGIN OU SENHA INCORRETOS")


        api = Videolog("<api_url>", "0123my_token")
        with self.assertRaises(ValueError):
            api.login("<incorrect_login>", "<incorrect_passwd>")

    @fudge.patch('httplib.HTTPConnection')
    def test_can_recover_from_response_error(self, HTTPConnection):
        headers = {
            'Token': '0123my_token',
            'Content-type': 'application/x-www-form-urlencoded',
        }

        self.httpconnection_mock(HTTPConnection, 'POST', '<api_url>',
                                 '/usuario/login', arg.any(),
                                 headers, None, httplib.INTERNAL_SERVER_ERROR)

        api = Videolog("<api_url>", "0123my_token")
        with self.assertRaises(APIError):
            api.login("<login>", "<passwd>")
