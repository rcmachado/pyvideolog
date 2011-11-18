import unittest2
import fudge
from fudge.inspector import arg

from videolog.videolog import Videolog

class VideologTestCase(unittest2.TestCase):
    def setUp(self):
        fudge.clear_calls()
        fudge.clear_expectations()

    def tearDown(self):
        fudge.verify()

    @fudge.patch('httplib.HTTPConnection')
    def test_can_login(self, HTTPConnection):
        headers = {
            'Token': '0123my_token'
        }
        (HTTPConnection.expects_call()
            .with_args("<api_url>").returns_fake()
            .expects("request")
            .with_matching_args("POST", "/usuario/login", arg.any(), headers)
            .expects("getresponse")
            .returns_fake()
            .expects("read")
            .returns("Autenticacao=HASHAUTENTICACAO"))

        api = Videolog("<api_url>", "0123my_token")
        self.assertTrue(api.login("<login>", "<senha>"))
