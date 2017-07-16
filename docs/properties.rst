.. _properties:

Properties
==========

Guessed values are cleaned up and given in a readable format
which may not match exactly the raw filename.

So, for instance,

- ``DVDSCR`` will be guessed as ``source`` = ``DVD`` + ``other`` = ``Screener``
- ``1920x1080`` will be guessed as ``screen_size`` = ``1080p``
- ``DD5.1`` will be guessed as ``audio_codec`` = ``Dolby Digital`` + ``audio_channels`` = ``5.1``


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
    ``qt``, ``ra``, ``ram``, ``rm``, ``srt``, ``ssa``, ``sub``, ``torrent``, ``ts``, ``vob``, ``wav``, ``webm``,
    ``wma``, ``wmv``


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

  - ``Bonus``, ``Extras``, ``Final``, ``Pilot``, ``Special``, ``Unaired``


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

- **source**

  Source of the release

  - ``Analogue HDTV``, ``Blu-ray``, ``Camera``, ``Digital TV``, ``DVD``, ``HD Camera``, ``HD Telecine``,
    ``HD Telesync``, ``HD-DVD``, ``HDTV``, ``Pay-per-view``, ``Satellite``, ``Telecine``, ``Telesync``, ``TV``,
    ``Ultra HD Blu-ray``, ``Ultra HDTV``, ``VHS``, ``Video on Demand``, ``Web``, ``Workprint``


- **screen_size**

  Resolution of video.

  - ``<width>x<height>``, ``360i``, ``360p``, ``368p``, ``480i``, ``480p``, ``576i``, ``576p``, ``720p``, ``900i``,
    ``900p``, ``1080i``, ``1080p``, ``2160p``, ``4320p``


- **video_codec**

  Codec used for video.

  - ``DivX``, ``H.264``, ``H.265``, ``MPEG-2``, ``RealVideo``, ``Xvid``


- **video_profile**

  Codec profile used for video.

  - ``Baseline``, ``High``, ``High 10``, ``High 4:2:2``, ``High 4:4:4 Predictive``, ``Main``, ``Extended``


- **color_depth**

  Bit depth used for video.
  - ``8-bit``, ``10-bit``, ``12-bit``


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

  - ``AAC``, ``Dolby Atmos``, ``Dolby Digital``, ``Dolby Digital Plus``, ``Dolby TrueHD``, ``DTS``,  ``FLAC``, ``MP3``


- **audio_profile**

  The codec profile used for audio.

  - ``High Efficiency``, ``High Quality``, ``Low Complexity``, ``Master Audio``


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

  - ``Alternative Cut``, ``Collector``, ``Criterion``, ``Deluxe``, ``Director's Cut``, ``Director's Definitive Cut``,
    ``Extended``, ``Festival``, ``IMAX``, ``Remastered``, ``Special``, ``Limited``, ``Theatrical``, ``Ultimate``,
    ``Uncensored``, ``Uncut``, ``Unrated``


- **film**

  Film number of this movie.


- **film_title**

  Film title of this movie.


- **film_series**

  Film series of this movie.


- **other**

  Other property will appear under this property.

  - ``3D``, ``Audio Fixed``, ``Bonus``, ``BT.2020``, ``Classic``, ``Colorized``, ``Complete``, ``Converted``,
    ``Documentary``, ``Dolby Vision``, ``Dual Audio``, ``East Coast Feed``, ``Fan Subtitled``, ``Fast Subtitled``,
    ``Full HD``, ``Hardcoded Subtitles``, ``HD``, ``HDR10``, ``High Quality``, ``High Resolution``, ``Internal``,
    ``Line Dubbed``, ``Line Audio``, ``Mic Dubbed``, ``Micro HD``, ``Mux``, ``NTSC``, ``Open Matte``,
    ``Original Aspect Ratio``, ``Original Video``, ``PAL``, ``Preair``, ``Proper``, ``PS Vita``, ``Read NFO``,
    ``Region 5``, ``Region C``, ``Reencoded``, ``Remux``, ``Retail``, ``Rip``, ``Screener``, ``SECAM``,
    ``Standard Dynamic Range``, ``Straight to Video``, ``Sync Fixed``, ``Trailer``, ``Ultra HD``, ``Upscaled``,
    ``West Coast Feed``, ``Widescreen``, ``XXX``

