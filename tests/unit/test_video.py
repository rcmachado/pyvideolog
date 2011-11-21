# -*- coding: utf-8 -*-
from datetime import datetime
import httplib
import urllib
import json

import unittest2
import fudge

from videolog.video import Video
from tests.unit.testcase import BaseTestCase

class VideoTestCase(BaseTestCase):
    def setUp(self):
        fudge.clear_calls()
        fudge.clear_expectations()

    def tearDown(self):
        fudge.verify()

    @fudge.patch('httplib.HTTPConnection')
    def test_search_for_video(self, HTTPConnection):
        expected_response = [
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

        headers = {"Token": "0123token"}
        params = {"q":"cool video"}

        self.httpconnection_mock(HTTPConnection, 'GET', '<api_url>',
                                 '/video/busca.json', params,
                                 headers, json.dumps(expected_response))

        video_api = Video("<api_url>", "0123token")
        videos = video_api.search("cool video")

        criacao = datetime.strptime("2009-03-14T08:07:38", "%Y-%m-%dT%H:%M:%S")
        self.assertEqual(videos[0]['criacao'], criacao)

    def test_search_for_video_without_params_raises_error(self):
        video_api = Video("<api_url>", "0123token")
        with self.assertRaises(ValueError):
            videos = video_api.search()