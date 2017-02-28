.. _properties:

Properties
==========

Guessed values are cleaned up and given in a readable format
which may not match exactly the raw filename.

So, for instance,

- ``DVDSCR`` will be guessed as ``format`` = ``DVD`` + ``other`` = ``Screener``
- ``1920x1080`` will be guessed as ``screenSize`` = ``1080p``
- ``DD5.1`` will be guessed as ``audioCodec`` = ``DolbyDigital`` + ``audioChannel`` = ``5.1``


Main properties
---------------

- **type**

  Type of the file.

  - ``unknown``, ``movie``, ``episode``, ``moviesubtitle``, ``episodesubtitle``


- **title**

  Title of movie or episode.

- **alternative_title**

  Other titles found for movie.

- **container**

  Container of the file.

  - ``3g2``, ``wmv``, ``webm``, ``mp4``, ``avi``, ``mp4a``, ``mpeg``, ``sub``, ``mka``, ``m4v``, ``ts``, ``mkv``, ``ra``, ``rm``, ``wma``, ``ass``, ``mpg``, ``ram``, ``3gp``, ``ogv``, ``mov``, ``ogm``, ``asf``, ``divx``, ``ogg``, ``ssa``, ``qt``, ``idx``, ``nfo``, ``wav``, ``flv``, ``3gp2``, ``iso``, ``mk2``, ``srt``

- **mimetype**

  Mime type of the related container. Guessed values may vary based on OS native support of mime type.


- **date**

  Date found in filename.


- **year**

  Year of movie (or episode).


- **release_group**

  Name of (non)scene group that released the file.


- **website**

  Name of website contained in the filename.

- **streaming_service**

  Name of the streaming service (``Netflix``, ``Comedy Central``, ...)

Episode properties
------------------

- **season**

  Season number. (Can be a list if several are found)


- **episode**

  Episode number. (Can be a list if several are found)


- **episode_count**

  Total number of episodes.


- **season_count**

  Total number of seasons.


- **episode_details**

  Some details about the episode.

  - ``Bonus`` ``Oav`` ``Ova`` ``Omake`` ``Extras`` ``Unaired`` ``Special`` ``Pilot``


- **episode_format**

  Episode format of the series.

  - ``Minisode``

- **part**

  Part number of the video. (Can be a list if several are found)


- **version**

  Version of the episode.

  - In anime fansub scene, new versions are released with tag ``<episode>v[0-9]``.


Video properties
----------------

- **format**

  Format of the initial source

  - ``TV`` ``HDTV`` ``UHDTV`` ``AHDTV`` ``HDTC`` ``SATRip`` ``WEB-DL`` ``VOD`` ``BluRay`` ``DVD`` ``WEBRip`` ``Workprint`` ``Telecine`` ``VHS`` ``DVB`` ``Telesync``  ``HD-DVD`` ``PPV`` ``Cam``

- **screen_size**

  Resolution of video.
  - ``720p`` ``1080p`` ``1080i`` ``<width>x<height>`` ``4K`` ``360p`` ``368p`` ``480p`` ``576p`` ``900p``


- **video_codec**
  Codec used for video.

  - ``h264`` ``h265`` ``DivX`` ``XviD`` ``Real`` ``Mpeg2``


- **video_profile**
  Codec profile used for video.

  - ``8bit`` ``10bit`` ``HP`` ``BP`` ``MP`` ``XP`` ``Hi422P`` ``Hi444PP``


- **video_api**
  API used for the video.

  - ``DXVA``


Audio properties
----------------

- **audio_channels**

  Number of channels for audio.

  - ``1.0`` ``2.0`` ``5.1`` ``7.1``


- **audio_codec**
  Codec used for audio.

  - ``DTS`` ``TrueHD`` ``AAC`` ``AC3`` ``MP3`` ``Flac`` ``DolbyDigital``  ``DolbyAtmos``


- **audio_profile**
  The codec profile used for audio.

  - ``LC`` ``HQ`` ``HD`` ``HE`` ``HDMA``


Localization properties
-----------------------

- **country**

  Country(ies) of content. Often found in series, ``Shameless (US)`` for instance.

  - ``[<babelfish.Country>]`` (This class equals name and iso code)


- **language**

  Language(s) of the audio soundtrack.

  - ``[<babelfish.Language>]`` (This class equals name and iso code)


- **subtitle_language**

  Language(s) of the subtitles.

  - ``[<babelfish.Language>]`` (This class equals name and iso code)


Other properties
----------------

- **bonus**

  Bonus number.


- **bonus_title**

  Bonus title.


- **cd**

  CD number.


- **cd_count**

  Total count of CD.


- **crc32**

  CRC32 of the file.


- **uuid**

  Volume identifier (UUID).


- **size**

  Size (MB, GB, TB).


- **edition**

  Edition of the movie.

  - ``Special Edition``, ``Collector Edition``, ``Director's cut``, ``Criterion Edition``, ``Deluxe Edition``, ``Theatrical Edition``


- **film**

  Film number of this movie.

- **film_title**

  Film title of this movie.

- **film_series**

  Film series of this movie.

- **other**

  Other property will appear under this property.

  - ``Fansub``, ``HR``, ``HQ``, ``Screener``, ``Unrated``, ``HD``, ``UltraHD``, ``3D``, ``SyncFix``, ``Bonus``,
  ``WideScreen``, ``Fastsub``, ``R5``, ``AudioFix``, ``DDC``, ``Trailer``, ``Complete``, ``Limited``, ``Classic``,
  ``Proper``, ``DualAudio``, ``LiNE``, ``LD``, ``MD``, ``XXX``, ``Remastered``, ``Extended``, ``Extended Cut``,
  ``Alternative Cut``, ``Uncut``, ``Retail``, ``ReEncoded``, ``Mux``, ``Hardcoded Subtitles``, ``Converted``,
  ``Colorized``, ``Documentary``, ``Festival``, ``FINAL``, ``Internal``, ``Open Matte``, ``Read NFO``

