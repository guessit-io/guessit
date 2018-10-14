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

  - ``A&E``, ``ABC``, ``ABC Australia``, ``Adult Swim``, ``Al Jazeera English``, ``AMC``, ``America's Test Kitchen``,
    ``Amazon Prime``, ``Animal Planet``, ``AnimeLab``, ``AOL``, ``ARD``, ``BBC iPlayer``, ``BravoTV``, ``Canal+``,
    ``Cartoon Network``, ``CBC``, ``CBS``, ``Channel 4``, ``CHRGD``, ``Cinemax``, ``CNBC``, ``Comedy Central``,
    ``Comedians in Cars Getting Coffee``, ``Country Music Television``, ``Crackle``, ``Crunchy Roll``, ``CSpan``,
    ``CTV``, ``CuriosityStream``, ``CWSeed``, ``Daisuki``, ``Deadhouse Films``, ``Digiturk Diledigin Yerde``,
    ``Discovery``, ``DIY Network``, ``Disney``, ``Doc Club``, ``DPlay``, ``E!``, ``ePix``, ``El Trece``, ``ESPN``,
    ``Esquire``, ``Family``, ``Family Jr``, ``Food Network``, ``Fox``, ``Freeform``, ``FYI Network``, ``Global``,
    ``GloboSat Play``, ``Hallmark``, ``HBO Go``, ``HGTV``, ``History``, ``Hulu``, ``Investigation Discovery``, ``IFC``,
    ``iTunes``, ``ITV``, ``Knowledge Network``, ``Lifetime``, ``Motor Trend OnDemand``, ``MSNBC``, ``MTV``,
    ``National Geographic``, ``NBA TV``, ``NBC``, ``Netflix``, ``NFL``, ``NFL Now``, ``NHL GameCenter``,
    ``Nickelodeon``, ``Norsk Rikskringkasting``, ``PBS``, ``PBS Kids``, ``Playstation Network``, ``Pluzz``, ``RTE One``,
    ``SBS (AU)``, ``SeeSo``, ``Shomi``, ``Spike``, ``Spike TV``, ``Sportsnet``, ``Sprout``, ``Stan``, ``Starz``,
    ``Sveriges Television``, ``SwearNet``, ``Syfy``, ``TBS``, ``TFou``, ``The CW``, ``TLC``, ``TubiTV``,
    ``TV3 Ireland``, ``TV4 Sweeden``, ``TV Land``, ``UFC``, ``UKTV``, ``Univision``, ``USA Network``, ``Velocity``,
    ``VH1``, ``Viceland``, ``Vimeo``, ``VRV``, ``W Network``, ``WatchMe``, ``WWE Network``, ``Xbox Video``, ``Yahoo``,
    ``YouTube Red``, ``ZDF``


Episode properties
------------------

- **season**

  Season number. (Can be a list if several are found)


- **episode**

  Episode number. (Can be a list if several are found)


- **disc**

  Disc number. (Can be a list if several are found)


- **episode_count**

  Total number of episodes.


- **season_count**

  Total number of seasons.


- **episode_details**

  Some details about the episode.

  - ``Final``, ``Pilot``, ``Special``, ``Unaired``


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

  - ``Analog HDTV``, ``Blu-ray``, ``Camera``, ``Digital Master``, ``Digital TV``, ``DVD``, ``HD Camera``,
    ``HD Telecine``, ``HD Telesync``, ``HD-DVD``, ``HDTV``, ``Pay-per-view``, ``Satellite``, ``Telecine``, ``Telesync``,
    ``TV``, ``Ultra HD Blu-ray``, ``Ultra HDTV``, ``VHS``, ``Video on Demand``, ``Web``, ``Workprint``


- **screen_size**

  Resolution of video.

  - ``<width>x<height>``, ``360i``, ``360p``, ``368p``, ``480i``, ``480p``, ``576i``, ``576p``, ``720p``, ``900i``,
    ``900p``, ``1080i``, ``1080p``, ``1440p``, ``2160p``, ``4320p``


- **aspect_ratio**

  Aspect ratio of video. Calculated using width and height from ``screen_size``


- **video_codec**

  Codec used for video.

  - ``DivX``, ``H.263``, ``H.264``, ``H.265``, ``MPEG-2``, ``RealVideo``, ``VP7``, ``VP8``, ``VP9``,``Xvid``


- **video_profile**

  Codec profile used for video.

  - ``Baseline``, ``High``, ``High 10``, ``High 4:2:2``, ``High 4:4:4 Predictive``, ``Main``, ``Extended``


- **color_depth**

  Bit depth used for video.
  - ``8-bit``, ``10-bit``, ``12-bit``


- **video_api**

  API used for the video.

  - ``DXVA``


- **video_bit_rate**

  Video bit rate (Mbps). Examples: ``25Mbps`` (``<BitRate [25Mbps]>``), ``40Mbps`` (``<BitRate [40Mbps]>``).

  - ``[<guessit.BitRate>]`` (object has ``magnitude`` and ``units``)


- **frame_rate**

  Video frame rate (frames per second).
  Examples: ``25fps`` (``<FrameRate [25fps]>``), ``60fps`` (``<FrameRate [60fps]>``).

  - ``[<guessit.FrameRate>]`` (object has ``magnitude`` and ``units``)


Audio properties
----------------

- **audio_channels**

  Number of channels for audio.

  - ``1.0``, ``2.0``, ``5.1``, ``7.1``


- **audio_codec**

  Codec used for audio.

  - ``AAC``, ``Dolby Atmos``, ``Dolby Digital``, ``Dolby Digital Plus``, ``Dolby TrueHD``, ``DTS``,  ``FLAC``, ``LPCM``,
    ``MP3``, ``Opus``, ``PCM``, ``Vorbis``


- **audio_profile**

  The codec profile used for audio.

  - ``Extended Surround``, ``EX``, ``High Efficiency``, ``High Quality``, ``High Resolution Audio``, ``Low Complexity``,
    ``Master Audio``


- **audio_bit_rate**

  Audio bit rate (Kbps, Mbps). Examples: ``448Kbps`` (``<BitRate [448Kbps]>``), ``1.5Mbps`` (``<BitRate [1.5Mbps]>``).

  - ``[<guessit.BitRate>]`` (object has ``magnitude`` and ``units``)


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

  Size (MB, GB, TB). Examples: ``1.2GB`` (``<Size [1.2GB]>``), ``430MB`` (``<Size [430MB]>``).

  - ``[<guessit.Size>]`` (object has ``magnitude`` and ``units``)


- **edition**

  Edition of the movie.

  - ``Alternative Cut``, ``Collector``, ``Criterion``, ``Deluxe``, ``Director's Cut``, ``Director's Definitive Cut``,
    ``Extended``, ``Fan``, ``Festival``, ``IMAX``, ``Remastered``, ``Special``, ``Limited``, ``Theatrical``,
    ``Ultimate``, ``Uncensored``, ``Uncut``, ``Unrated``


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
    ``Full HD``, ``Hardcoded Subtitles``, ``HD``, ``HDR10``, ``High Frame Rate``, ``High Quality``, ``High Resolution``,
    ``Internal``, ``Line Dubbed``, ``Line Audio``, ``Mic Dubbed``, ``Micro HD``, ``Mux``, ``NTSC``, ``Obfuscated``,
    ``Open Matte``, ``Original Aspect Ratio``, ``Original Video``, ``PAL``, ``Preair``, ``Proof``, ``Proper``,
    ``PS Vita``, ``Read NFO``, ``Region 5``, ``Region C``, ``Reencoded``, ``Remux``, ``Repost``, ``Retail``, ``Rip``,
    ``Sample``, ``Screener``, ``SECAM``, ``Standard Dynamic Range``, ``Straight to Video``, ``Sync Fixed``, ``Trailer``,
    ``Ultra HD``, ``Upscaled``, ``West Coast Feed``, ``Widescreen``, ``XXX``

