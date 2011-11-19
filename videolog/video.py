import urllib
import json

from videolog.core import Videolog

class Video(Videolog):
    def search(self, term, user_id=None):
        headers = {
            "Token": self._token,
        }

        params = {'q': term}

        content = self._make_request('GET', '/video/busca.json', params, headers)
        return json.loads(content)
