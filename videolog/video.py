from datetime import datetime
import json
import os
import logging
import mimetypes

import simplexml

from videolog.core import Videolog, APIError

_logger = logging.getLogger('videolog')

class Video(Videolog):
    PUBLIC = "0"
    FRIENDS = "1"
    PRIVATE = "2"

    def search(self, term=None, channel=None, user_id=None, limit=None,
        offset=None, metatags=None):
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
            if video['mobile'].lower() == 's':
                video['mobile'] = True
            else:
                video['mobile'] = False
            response.append(video)

        return response

    def info(self, video_id):
        content = self._make_request('GET', '/video/%s.json' % video_id)
        result = json.loads(content)
        video = result['video']
        video['criacao'] = datetime.strptime(video['criacao'], "%Y-%m-%dT%H:%M:%S")
        if video['mobile'].lower() == 's':
            video['mobile'] = True
        else:
            video['mobile'] = False

        return video

    def upload(self, file_name, dirname, title, description, channel, privacy=0, metatags=''):
        video_dados = {
            'video': {
                'titulo': title,
                'descricao': description,
                'canal': channel,
                'privacidade': privacy,
                'metatags': metatags
            }
        }

        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        content    = self._make_request('POST', '/video.xml', params=simplexml.dumps(video_dados), headers=headers)
        video_uuid = simplexml.loads(content)['video']['uuid']

        file_path = "%s/%s" % (dirname.rstrip('/'), file_name)
        if not os.path.isfile(file_path):
            raise ValueError("File does not exist %s" % file_path)

        file_data = open(file_path).read()
        try:
            self.post_multipart(selector='/video/%s/upload' % video_uuid, files=(("video", file_name, file_data),), headers=headers)
            return True
        except APIError, e:
            _logger.info("Error uploading video %s: %s" % (file_name, e))
            return False

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

    def post_multipart(self, selector, files, headers):
        content_type, body = self.encode_multipart_formdata(files)

        headers['Content-Type'] = content_type

        self._make_request('POST', selector, params=body, headers=headers)

    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
