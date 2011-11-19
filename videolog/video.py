import urllib
import json

from videolog.base import Videolog

class Video(Videolog):
    def search(self, term, user_id=None):
        headers = {
            "Token": self._token,
        }

        params = {'q': term}

        encoded_params = urllib.urlencode(params)
        self._conn.request('GET', '/video/busca.json', encoded_params, headers)

        response = self._conn.getresponse()
        content = response.read()

        return json.loads(content)

