import httplib
import urllib

class Videolog(object):
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

        return content.split('=', 1)[1]
