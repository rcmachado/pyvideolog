# -*- coding: utf-8 -*-
from datetime import datetime
import json

import simplexml
import unittest2
import fudge

from videolog import video
from videolog.video import Video
from tests.unit.testcase import BaseTestCase

class VideoTestCase(BaseTestCase):
    @fudge.patch('httplib.HTTPConnection')
    def test_search_for_video(self, HTTPConnection):
        mock_response = [
            {
                "criacao": "2009-03-14T08:07:38",
                "privacidade": "0",
                "titulo": "Curso de Shell Script Parte 3 - Comando test",
                "usuario_id": 452174,
                "texto": "Curso de Shell Script Parte 3.1 - Comando testrnrn\n\n\nNícholas André - nicholasandreoliveira9@gmail.com\n\nwww.iotecnologia.com.br",
                "thumb": "http://videolog.tv/video_thumb.php?video=419763",
                "id": 419763,
                "url_mp4": "http://cdn-play1.videolog.tv/videos/0142e49a327d8832d44a93caf78cfb22/4ec6ddc7/6f/47/419763.flv",
                "id_canal": 18,
                "mobile": "N",
                "embed": "                 <iframe width='560' height=315 src='http://embed.videolog.tv/v/index.php?id_video=419763&width=560&height=315' scrolling='no' frameborder='0' allowfullscreen></iframe>                 <p><a href='http://www.videolog.tv/video.php?id=419763'>Curso de Shell Script Parte 3 - Comando test</a> por <a href='http://www.videolog.tv/Blink182br'> Blink182br </a> no <a href='http://www.videolog.tv'>Videolog.tv</a>.</p>               ",
                "link": "http://videolog.tv/video.php?id=419763",
                "visitas": 25652
            }
        ]

        expected_response = [
            {
                u"criacao": datetime.strptime("2009-03-14T08:07:38", "%Y-%m-%dT%H:%M:%S"),
                u"privacidade": u"0",
                u"titulo": u"Curso de Shell Script Parte 3 - Comando test",
                u"usuario_id": 452174,
                u"texto": u"Curso de Shell Script Parte 3.1 - Comando testrnrn\n\n\nNícholas André - nicholasandreoliveira9@gmail.com\n\nwww.iotecnologia.com.br",
                u"thumb": u"http://videolog.tv/video_thumb.php?video=419763",
                u"id": 419763,
                u"url_mp4": u"http://cdn-play1.videolog.tv/videos/0142e49a327d8832d44a93caf78cfb22/4ec6ddc7/6f/47/419763.flv",
                u"id_canal": 18,
                u"mobile": False,
                u"embed": u"                 <iframe width='560' height=315 src='http://embed.videolog.tv/v/index.php?id_video=419763&width=560&height=315' scrolling='no' frameborder='0' allowfullscreen></iframe>                 <p><a href='http://www.videolog.tv/video.php?id=419763'>Curso de Shell Script Parte 3 - Comando test</a> por <a href='http://www.videolog.tv/Blink182br'> Blink182br </a> no <a href='http://www.videolog.tv'>Videolog.tv</a>.</p>               ",
                u"link": u"http://videolog.tv/video.php?id=419763",
                u"visitas": 25652
            }
        ]

        headers = {"Token": "0123token"}
        params = {"q":"cool video"}

        self.httpconnection_mock(HTTPConnection, 'GET', '<api_url>',
                                 '/video/busca.json', params,
                                 headers, json.dumps(mock_response))

        video_api = Video("<api_url>", "0123token")
        videos = video_api.search("cool video")

        self.assertEqual(videos, expected_response)

    def test_search_for_video_without_params_raises_error(self):
        video_api = Video("<api_url>", "0123token")
        with self.assertRaises(ValueError):
            videos = video_api.search()

    @fudge.patch('httplib.HTTPConnection')
    def test_can_upload_video(self, HTTPConnection):
        expected_response = {"video": {"uuid": "shouldBeUUID"}}

        file_name = 'ShouldBeFileName'
        dirname = 'ShouldBeDirName'
        title = 'ShouldBeTitle'
        description = 'ShouldBeDescription'
        channel = 'ShouldBeChannel'
        privacy = 0
        metatags = 'ShouldBeMetatags'

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
            'Token': 'shouldBeToken',
            'Autenticacao': 'shouldBeAuth',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        self.httpconnection_mock(HTTPConnection, 'POST', '<api_url>', '/video.xml', simplexml.dumps(video_dados), headers, simplexml.dumps(expected_response))

        video_api = Video("<api_url>", "shouldBeToken")
        video_api._auth_hash = 'shouldBeAuth'
        video_api.post_multipart = fudge.Fake(callable=True)

        os_fake = fudge.Fake(callable=True)
        os_fake.path = fudge.Fake(callable=True)
        os_fake.path.isfile = fudge.Fake(callable=True).returns(True)

        with fudge.patched_context(video, "os", os_fake):
            with fudge.patch("__builtin__.open") as open_fake:
                open_fake.is_callable().with_args('ShouldBeDirName/ShouldBeFileName').returns_fake().expects('read').returns('shouldBeFileData')

                video_upload = video_api.upload(file_name=file_name, dirname=dirname, title=title, description=description, channel=channel, privacy=privacy, metatags=metatags)

        self.assertTrue(video_upload)
