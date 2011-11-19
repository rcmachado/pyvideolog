import unittest2
import fudge
from fudge.inspector import arg

from videolog.core import Videolog

class VideologTestCase(unittest2.TestCase):
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
        (HTTPConnection.expects_call()
            .with_args("<api_url>").returns_fake()
            .expects("request")
            .with_args("POST", "/usuario/login", arg.any(), headers)
            .expects("getresponse")
            .returns_fake()
            .expects("read")
            .returns("Autenticacao=HASHAUTENTICACAO"))

        api = Videolog("<api_url>", "0123my_token")
        self.assertTrue(api.login("<login>", "<senha>"))

    @fudge.patch('httplib.HTTPConnection')
    def test_can_not_login_with_invalid_user(self, HTTPConnection):
        headers = {
            'Token': '0123my_token',
            'Content-type': 'application/x-www-form-urlencoded',
        }
        (HTTPConnection.expects_call()
            .with_args("<api_url>").returns_fake()
            .expects("request")
            .with_args("POST", "/usuario/login", arg.any(), headers)
            .expects("getresponse")
            .returns_fake()
            .expects("read")
            .returns("LOGIN OU SENHA INCORRETOS"))

        api = Videolog("<api_url>", "0123my_token")
        with self.assertRaises(ValueError):
            api.login("<incorrect_login>", "<incorrect_passwd>")
