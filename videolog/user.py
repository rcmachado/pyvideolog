from datetime import datetime
import time
import json

from videolog.core import Videolog

class User(Videolog):
    def find_videos(self, user):
        content = self._make_request('GET', '/usuario/%s/videos.json' % user)
        usuario = json.loads(content)

        response = []
        for video in usuario['usuario']['videos']:
            video['criacao'] = datetime.strptime(video['criacao'], "%Y-%m-%dT%H:%M:%S")
            video["duracao"] = time.strptime("00:00:05", "%H:%M:%S")
            if video['mobile'].lower() == "s":
                video['mobile'] = True
            else:
                video['mobile'] = False
            response.append(video)
        return response