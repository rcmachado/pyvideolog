from datetime import datetime
import urllib
import json

from videolog.core import Videolog

class Video(Videolog):
    PUBLICO = "0"
    AMIGOS = "1"
    PRIVADO = "2"

    def search(self, term, user_id=None):
        params = {'q': term}

        content = self._make_request('GET', '/video/busca.json', params)
        result = json.loads(content)

        response = []
        for video in result:
            video['criacao'] = datetime.strptime(video['criacao'], "%Y-%m-%dT%H:%M:%S")
            response.append(video)

        return response
