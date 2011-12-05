import httplib
import logging
import urllib

_logger = logging.getLogger('videolog')

class APIError(Exception):
    pass

class Videolog(object):
    _auth_hash = None

    def __init__(self, url, token):
        self._url = url
        self._token = token
        self._conn = httplib.HTTPConnection(self._url)

    def _make_request(self, method, path, params=None, headers=dict()):
        full_headers = dict(headers)
        full_headers['Token'] = self._token
        if self._auth_hash:
            full_headers['Autenticacao'] = self._auth_hash

        if type(params) == dict:
            params = urllib.urlencode(params)
        if params is not None:
            params = str(params)

        _logger.debug("Make request to %s%s" % (self._url, str(path)))
        self._conn.request(method, str(path), params, full_headers)
        response = self._conn.getresponse()

        if response.status != httplib.OK:
            raise APIError("Request error: %s" % response.status)

        return response.read()

    def login(self, login, passwd):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
        }

        params = {'login': login, 'senha': passwd}
        content = self._make_request('POST', '/usuario/login', params, headers)

        if content == "LOGIN OU SENHA INCORRETOS":
            raise ValueError("Incorrect login and password")

        _logger.info("Logged in API using %s as login" % login)
        self._auth_hash = content.split('=', 1)[1]
        return True
