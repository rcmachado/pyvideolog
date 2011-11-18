import httplib
import urllib

class Videolog(object):
    _auth_hash = None

    def __init__(self, url, token):
        self._url = url
        self._token = token
        self._conn = httplib.HTTPConnection(self._url)

    def login(self, login, passwd):
        headers = {
            "Token": self._token,
            "Content-type": "application/x-www-form-urlencoded",
        }

        params = urllib.urlencode({'login': login, 'senha': passwd})
        self._conn.request('POST', '/usuario/login', params, headers)

        response = self._conn.getresponse()
        content = response.read()

        if content == "LOGIN OU SENHA INCORRETOS":
            raise ValueError("Incorrect login and password")

        self._auth_hash = content.split('=', 1)[1]
        return True
