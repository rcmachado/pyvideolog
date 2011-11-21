<<<<<<< HEAD
from videolog.videolog import Videolog
import simplexml
import httplib
=======
from datetime import datetime
import urllib
import json

from videolog.core import Videolog
>>>>>>> 01cb29df936d6872cd921f634d21f49e859cfe6f

class Video(Videolog):
    PUBLICO = "0"
    AMIGOS = "1"
    PRIVADO = "2"

    def search(self, term=None, channel=None, user_id=None, limit=None, offset=None,
        metatags=None):
        params = dict()

        if term is not None:
            params['q'] = term

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

        if not params:
            raise ValueError("You need to specify at least one criteria")

        content = self._make_request('GET', '/video/busca.json', params)
        result = json.loads(content)

        response = []
        for video in result:
            video['criacao'] = datetime.strptime(video['criacao'], "%Y-%m-%dT%H:%M:%S")
            response.append(video)

<<<<<<< HEAD
    def __init__(self):
        pass

    def upload(self, file_path):
        
        video_dados = {
            'videos': {
                'titulo': '',
                'descricao': '',
                'canal': 2,
                'privavidade': 2,
                'metatags': ''
            }
        }
        headers = {
            'Token': self._token,
            'Autenticacao': '',
            'Content-Type': "application/x-www-form-urlencoded"
        }

        self._conn.request('POST', '/video.xml', body=simplexml.dumps(video_dados), headers=headers)
        response = self._conn.getresponse()
        content = response.read()

        status, reason, content = self.post_multipart(host='api.videolog.tv', selector='/video/%s/upload' % video_uuid, files=(("video", file_name, file_data),), headers=headers)
        
        if status == 200:
            print "[videolog] - Upload realizado com sucesso %s, %s" % (status, content)
            return

    def encode_multipart_formdata(self, files):
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def post_multipart(self, host, selector, files, headers):
        content_type, body = self.encode_multipart_formdata(files)
        h = httplib.HTTPConnection(host)

        headers['Content-Type'] = content_type
        
        print "[videolog] - post multipart %s" % (headers)

        h.request('POST', selector, body, headers)
        res = h.getresponse()

        return res.status, res.reason, res.read()
        
=======
        return response
>>>>>>> 01cb29df936d6872cd921f634d21f49e859cfe6f
