from videolog.videolog import Videolog
import simplexml
import httplib

class Video(Videolog):

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
        
