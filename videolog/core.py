import httplib
import urllib

class APIError(Exception):
    pass

class Videolog(object):
    _auth_hash = None

    def __init__(self, url, token):
        self._url = url
        self._token = token
        self._conn = httplib.HTTPConnection(self._url)

    def _make_request(self, method, path, params, headers):
        full_headers = dict(headers)
        full_headers['Token'] = self._token
        if self._auth_hash:
            full_headers['Autenticacao'] = self._auth_hash

        encoded_params = urllib.urlencode(params)
        self._conn.request(method, path, encoded_params, full_headers)
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

        self._auth_hash = content.split('=', 1)[1]
        return True
