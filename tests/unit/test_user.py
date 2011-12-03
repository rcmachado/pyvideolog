from datetime import datetime
import time
import json

import fudge
import unittest2

from videolog.user import User
from videolog.video import Video
from tests.unit.testcase import BaseTestCase

class UserTestCase(BaseTestCase):
    def setUp(self):
        fudge.clear_calls()
        fudge.clear_expectations()

    def tearDown(self):
        fudge.verify()

    @fudge.patch('httplib.HTTPConnection')
    def test_list_videos_from_user(self, HTTPConnection):
        headers = {'Token': '0123token'}

        mock_response = {
            "usuario": {
                "paginas": 1,
                "videos": [
                    {
                        "criacao": "2011-11-21T11:51:07",
                        "uri": "/video/722934.json",
                        "privacidade": "2",
                        "titulo": "Quicktime sample",
                        "usuario_id": 844849,
                        "texto": "quicktime",
                        "thumb": "http://videolog.tv/video_thumb.php?video=722934",
                        "id": 722934,
                        "url_mp4": "http://cdn-play1.videolog.tv/videos/7fbde14dbe292b81f8a591d27f3aeec8/4ecac979/49/da/722934.mp4",
                        "id_canal": 18,
                        "mobile": "S",
                        "embed": "                 <iframe width='560' height=315 src='http://embed.videolog.tv/v/index.php?id_video=722934&width=560&height=315' scrolling='no' frameborder='0' allowfullscreen></iframe>                 <p><a href='http://www.videolog.tv/video.php?id=722934'>Quicktime sample</a> por <a href='http://www.videolog.tv/rcmachado2'> rcmachado2 </a> no <a href='http://www.videolog.tv'>Videolog.tv</a>.</p>               ",
                        "link": "http://videolog.tv/video.php?id=722934",
                        "visitas": 3,
                        "uri_comentarios": "/video/722934/comentarios.json",
                        "uri_videos_relacionados": "/video/722934/videosRelacionados.json",
                        "duracao": "00:00:05"
                    }
                ],
                "id": 844849,
                "login": "rcmachado2"
            }
        }

        expected_response = [
            {
                u"criacao": datetime.strptime("2011-11-21T11:51:07", "%Y-%m-%dT%H:%M:%S"),
                u"uri": u"/video/722934.json",
                u"privacidade": u"2",
                u"titulo": u"Quicktime sample",
                u"usuario_id": 844849,
                u"texto": u"quicktime",
                u"thumb": u"http://videolog.tv/video_thumb.php?video=722934",
                u"id": 722934,
                u"url_mp4": u"http://cdn-play1.videolog.tv/videos/7fbde14dbe292b81f8a591d27f3aeec8/4ecac979/49/da/722934.mp4",
                u"id_canal": 18,
                u"mobile": True,
                u"embed": u"                 <iframe width='560' height=315 src='http://embed.videolog.tv/v/index.php?id_video=722934&width=560&height=315' scrolling='no' frameborder='0' allowfullscreen></iframe>                 <p><a href='http://www.videolog.tv/video.php?id=722934'>Quicktime sample</a> por <a href='http://www.videolog.tv/rcmachado2'> rcmachado2 </a> no <a href='http://www.videolog.tv'>Videolog.tv</a>.</p>               ",
                u"link": u"http://videolog.tv/video.php?id=722934",
                u"visitas": 3,
                u"uri_comentarios": u"/video/722934/comentarios.json",
                u"uri_videos_relacionados": u"/video/722934/videosRelacionados.json",
                u"duracao": time.strptime("00:00:05", "%H:%M:%S")
            }
        ]

        self.httpconnection_mock(HTTPConnection, "GET", '<api_url>',
                                 '/usuario/844849/videos.json?privacidade=2', None,
                                 headers, json.dumps(mock_response))

        user_api = User("<api_url>", "0123token")
        videos = user_api.find_videos(user=844849, privacy=Video.PRIVATE)

        self.assertEqual(videos, expected_response)
