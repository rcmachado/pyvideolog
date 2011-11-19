pyvideolog
==========

Módulo Python para acesso à API do [Videolog](http://videolog.tv/ "Videolog").
A API do módulo ainda está incompleta e pode sofrer modificações até a versão
1.0 (que ainda deve demorar um bom tempo até aparecer)

Pré-requisitos
--------------

- Python 2.6+

Exemplos
--------

    $ python
    >>> from videolog.video import Video
    >>> video = Video("api-url", "token")
    >>> video.search("cool video")
    []

Licença
-------

Licenciado sob os termos da [MIT License](http://www.opensource.org/licenses/mit-license.php).
Para detalhes, consulte o arquivo LICENSE-MIT
