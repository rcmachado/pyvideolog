import httplib
import urllib

import unittest2
import fudge

class BaseTestCase(unittest2.TestCase):
    def setUp(self):
        fudge.clear_calls()
        fudge.clear_expectations()

    def tearDown(self):
        fudge.verify()

    def httpconnection_mock(self, HTTPConnection, method, url, path, params,
        headers, response, status=httplib.OK):

        if type(params) == dict:
            params = urllib.urlencode(params)

        (HTTPConnection.expects_call()
            .with_args(url).returns_fake()
            .expects("request")
            .with_args(method, str(path), params, headers)
            .expects("getresponse")
            .returns_fake()
            .has_attr(status=status)
            .provides("read")
            .returns(response))
