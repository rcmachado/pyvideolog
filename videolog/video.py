from datetime import datetime
import urllib
import json

from videolog.core import Videolog

class Video(Videolog):
    PUBLICO = "0"
    AMIGOS = "1"
    PRIVADO = "2"

    def search(self, term, channel=None, user_id=None, limit=None, offset=None,
        metatags=None):
        params = {'q': term}

        if channel is not None:
            params['canal'] = int(channel)

        if user_id is not None and int(user_id) != 0:
            params['usuario'] = int(user_id)

        if limit is not None and int(limit) != 0:
            params['itens'] = int(limit)

        if offset is not None:
            params['inicio'] = int(offset)

        if metatags:
            tags = []
            for metatag in metatags:
                tags.append("%s:%s" % metatag[0], metatag[1])
            params['metatags'] = ",".join(tags)

        content = self._make_request('GET', '/video/busca.json', params)
        result = json.loads(content)

        response = []
        for video in result:
            video['criacao'] = datetime.strptime(video['criacao'], "%Y-%m-%dT%H:%M:%S")
            response.append(video)

        return response
