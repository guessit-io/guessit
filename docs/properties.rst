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

  - ``episode``, ``movie``


- **title**

  Title of movie or episode.


- **alternative_title**

  Other titles found for movie.


- **container**

  Container of the file.

  - ``3g2``, ``3gp``, ``3gp2``, ``asf``, ``ass``, ``avi``, ``divx``, ``flv``, ``idx``, ``iso``, ``m4v``, ``mk2``,
    ``mkv``, ``mka``, ``mov``, ``mp4``, ``mp4a``, ``mpeg``, ``mpg``, ``nfo``, ``nzb``, ``ogg``, ``ogm``, ``ogv``,
    ``qt``, ``ra``, ``ram``, ``rm``, ``srt``, ``ssa``, ``sub``, ``torrent``, ``ts``, ``vob``, ``wav``, ``webm``, ``wma``,
    ``wmv``


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

  Name of the streaming service.

  - ``A&E``, ``ABC``, ``AMC``, ``Amazon Prime``, ``Adult Swim``, ``BBC iPlayer``, ``CBS``, ``Comedy Central``,
    ``Crunchy Roll``, ``The CW``, ``Discovery``, ``DIY Network``, ``Disney``, ``ePix``, ``HBO Go``, ``History``,
    ``Investigation Discovery``, ``IFC``, ``PBS``, ``National Geographic``, ``NBA TV``, ``NBC``, ``NFL``,
    ``Nickelodeon``, ``Netflix``, ``iTunes``, ``RTÉ One``, ``SeeSo``, ``Spike TV``, ``Syfy``, ``TFou``, ``TLC``,
    ``TV3 Ireland``, ``TV4 Sweeden``, ``TV Land``, ``UFC``, ``USA Network``


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

  - ``Bonus``, ``Extras``, ``Oav``, ``Ova``, ``Omake``, ``Pilot``, ``Special``, ``Unaired``


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

  - ``AHDTV``, ``BluRay``, ``Cam``, ``DVB``, ``DVD``, ``HD-DVD``, ``HDTC``, ``HDTV``, ``PPV``, ``SATRip``, ``Telecine``,
    ``Telesync``, ``TV``, ``UHDTV``, ``VHS``, ``VOD``, ``WEB-DL``, ``WEBRip``, ``Workprint``


- **screen_size**

  Resolution of video.

  - ``<width>x<height>``, ``360p``, ``368p``, ``480p``, ``576p``, ``720p``, ``1080p``, ``1080i``, ``900p``, ``4K``


- **video_codec**

  Codec used for video.

  - ``DivX``, ``h264``, ``h265``, ``Mpeg2``, ``Real``, ``XviD``


- **video_profile**

  Codec profile used for video.

  - ``8bit``, ``10bit``, ``BP``, ``Hi422P``, ``Hi444PP``, ``HP``, ``MP``, ``XP``


- **video_api**

  API used for the video.

  - ``DXVA``


Audio properties
----------------

- **audio_channels**

  Number of channels for audio.

  - ``1.0``, ``2.0``, ``5.1``, ``7.1``


- **audio_codec**

  Codec used for audio.

  - ``DTS`` ``TrueHD`` ``AAC`` ``AC3`` ``EAC3`` ``MP3`` ``Flac`` ``DolbyAtmos``


- **audio_profile**

  The codec profile used for audio.

  - ``HD``, ``HDMA``, ``HE``, ``HQ``, ``LC``


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

  - ``Collector Edition``, ``Criterion Edition``, ``Deluxe Edition``, ``Director's cut``,  ``Special Edition``,
    ``Limited Edition``, ``Theatrical Edition``


- **film**

  Film number of this movie.


- **film_title**

  Film title of this movie.


- **film_series**

  Film series of this movie.


- **other**

  Other property will appear under this property.

  - ``3D``, ``Alternative Cut``, ``AudioFix``, ``Bonus``, ``CC``, ``Classic``, ``Colorized``, ``Complete``,
    ``Converted``, ``Documentary``, ``DDC``, ``DualAudio``, ``East Coast Feed``, ``Extended``, ``Extended Cut``,
    ``Fansub``, ``Fastsub``, ``Festival``, ``FINAL``, ``FullHD``, ``Hardcoded Subtitles``, ``HD``, ``HDLight``, ``HQ``,
    ``HR``, ``Internal``, ``LD``, ``Limited``, ``LiNE``, ``MD``, ``mHD``, ``Mux``, ``NTSC``, ``Open Matte``,
    ``Original Aspect Ratio``, ``OV``, ``PAL``, ``Preair``, ``Proper``, ``PS Vita``, ``R5``, ``Read NFO``,
    ``ReEncoded``, ``Remastered``, ``Remux``, ``Retail``, ``Screener``, ``SECAM``, ``Straight to Video``, ``SyncFix``,
    ``Trailer``, ``UltraHD``, ``Uncensored``, ``Uncut``, ``Unrated``, ``West Coast Feed``, ``WideScreen``, ``XXX``

