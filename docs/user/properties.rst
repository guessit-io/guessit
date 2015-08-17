.. _properties:

Properties
~~~~~~~~~~

Guessed values are cleaned up and given in a readable format
which may not match exactly the raw filename.

So, for instance,

- ``DVDSCR`` will be guessed as ``format`` = ``DVD`` + ``other`` = ``Screener``
- ``1920x1080`` will be guessed as ``screenSize`` = ``1080p``
- ``DD5.1`` will be guessed as ``audioCodec`` = ``DolbyDigital`` + ``audioChannel`` = ``5.1``


Main properties
~~~~~~~~~~~~~~~

- **type**

  Type of the file.

  - ``unknown``, ``movie``, ``episode``, ``moviesubtitle``, ``episodesubtitle``


- **title**

  Title of movie or episode.

- **container**

  Container of the file.

  - ``3g2``, ``wmv``, ``webm``, ``mp4``, ``avi``, ``mp4a``, ``mpeg``, ``sub``, ``mka``, ``m4v``, ``ts``, ``mkv``, ``ra``, ``rm``, ``wma``, ``ass``, ``mpg``, ``ram``, ``3gp``, ``ogv``, ``mov``, ``ogm``, ``asf``, ``divx``, ``ogg``, ``ssa``, ``qt``, ``idx``, ``nfo``, ``wav``, ``flv``, ``3gp2``, ``iso``, ``mk2``, ``srt``


- **date**

  Date found in filename.


- **year**

  Year of movie (or episode).


- **releaseGroup**

  Name of (non)scene group that released the file.


- **website**

  Name of website contained in the filename.


Episode properties
~~~~~~~~~~~~~~~~~~

- **series**

  Name of series.


- **season**

  Season number.


- **episodeNumber**

  Episode number.


- **episodeList**

  List of episode numbers if several were found.

  - note: If several are found, ``episodeNumber`` is the first item of this list.


- **seasonList**

  List of season numbers if several were found.

  - note: If several are found, ``seasonNumber`` is the first item of this list.


- **episodeCount**

  Total number of episodes.


- **seasonCount**

  Total number of seasons.


- **episodeDetails**

  Some details about the episode.

  - ``Bonus`` ``Oav`` ``Ova`` ``Omake`` ``Extras`` ``Unaired`` ``Special`` ``Pilot``


- **episodeFormat**

  Episode format of the series.

  - ``Minisode``

- **part**

  Part number of the video.

- **partList**

List of part numbers if several were found.

- note: If several are found, ``part`` is the first item of this list.

- **version**

  Version of the episode.

  - In anime fansub scene, new versions are released with tag ``<episode>v[0-9]``.


Video properties
~~~~~~~~~~~~~~~~

- **format**

  Format of the initial source

  - ``HDTV`` ``WEB-DL`` ``TV`` ``VOD`` ``BluRay`` ``DVD`` ``WEBRip`` ``Workprint`` ``Telecine`` ``VHS`` ``DVB`` ``Telesync``  ``HD-DVD`` ``PPV`` ``Cam``


- **screenSize**

  Resolution of video.
  - ``720p`` ``1080p`` ``1080i`` ``<width>x<height>`` ``4K`` ``360p`` ``368p`` ``480p`` ``576p`` ``900p``


- **videoCodec**
  Codec used for video.

  - ``h264`` ``h265`` ``DivX`` ``XviD`` ``Real`` ``Mpeg2``


- **videoProfile**
  Codec profile used for video.

  - ``8bit`` ``10bit`` ``HP`` ``BP`` ``MP`` ``XP`` ``Hi422P`` ``Hi444PP``


- **videoApi**
  API used for the video.

  - ``DXVA``


Audio properties
~~~~~~~~~~~~~~~~

- **audioChannels**

  Number of channels for audio.

  - ``1.0`` ``2.0`` ``5.1`` ``7.1``


- **audioCodec**
  Codec used for audio.

  - ``DTS`` ``TrueHD`` ``DolbyDigital``  ``AAC`` ``AC3`` ``MP3`` ``Flac``


- **audioProfile**
  The codec profile used for audio.

  - ``LC`` ``HQ`` ``HD`` ``HE`` ``HDMA``


Localization properties
~~~~~~~~~~~~~~~~~~~~~~~

- **Country**

  Country(ies) of content. Often found in series, ``Shameless (US)`` for instance.

  - ``[<babelfish.Country>]`` (This class equals name and iso code)


- **Language**

  Language(s) of the audio soundtrack.

  - ``[<babelfish.Language>]`` (This class equals name and iso code)


- **subtitleLanguage**

  Language(s) of the subtitles.

  - ``[<babelfish.Language>]`` (This class equals name and iso code)


Other properties
~~~~~~~~~~~~~~~~

- **bonusNumber**

  Bonus number.


- **bonusTitle**

  Bonus title.


- **cdNumber**

  CD number.


- **cdNumberTotal**

  Total number of CD.


- **crc32**

  CRC32 of the file.


- **idNumber**

  Volume identifier (UUID).


- **edition**

  Edition of the movie.

  - ``Special Edition``, ``Collector Edition``, ``Director's cut``, ``Criterion Edition``, ``Deluxe Edition``


- **filmNumber**

  Film number of this movie.


- **filmSeries**

  Film series of this movie.

- **other**

  Other property will appear under this property.

  - ``Fansub``, ``HR``, ``HQ``, ``Netflix``, ``Screener``, ``Unrated``, ``HD``, ``3D``, ``SyncFix``, ``Bonus``, ``WideScreen``, ``Fastsub``, ``R5``, ``AudioFix``, ``DDC``, ``Trailer``, ``Complete``, ``Limited``, ``Classic``, ``Proper``, ``DualAudio``, ``LiNE``, ``CC``, ``LD``, ``MD``

