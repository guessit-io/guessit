.. _advanced-configuration:

Advanced Configuration
======================
Guessit 3 supports advanced configuration of its internal parameters. This can be done using the
``-c``/``--config`` option. The provided config file should contain a section called ``advanced_config`` with all
parameters and values to be overridden.


Default Advanced Configuration
------------------------------
It's not possible to disable the default advanced configuration (``--no-embedded-config`` won't work for that).
This is by design since Guessit needs all these parameters in order to compile its internal rules and execute them.
Find bellow the internal advanced configuration parameters and their values:

.. code-block:: json

  "advanced_config": {
    "common_words": [
      "de",
      "it"
    ],
    "groups": {
      "starting": "([{",
      "ending": ")]}"
    },
    "container": {
      "subtitles": [
        "srt",
        "idx",
        "sub",
        "ssa",
        "ass"
      ],
      "info": [
        "nfo"
      ],
      "videos": [
        "3g2",
        "3gp",
        "3gp2",
        "asf",
        "avi",
        "divx",
        "flv",
        "m4v",
        "mk2",
        "mka",
        "mkv",
        "mov",
        "mp4",
        "mp4a",
        "mpeg",
        "mpg",
        "ogg",
        "ogm",
        "ogv",
        "qt",
        "ra",
        "ram",
        "rm",
        "ts",
        "wav",
        "webm",
        "wma",
        "wmv",
        "iso",
        "vob"
      ],
      "torrent": [
        "torrent"
      ],
      "nzb": [
        "nzb"
      ]
    },
    "country": {
      "synonyms": {
        "ES": [
          "españa"
        ],
        "GB": [
          "UK"
        ],
        "BR": [
          "brazilian",
          "bra"
        ],
        "CA": [
          "québec",
          "quebec",
          "qc"
        ],
        "MX": [
          "Latinoamérica",
          "latin america"
        ]
      }
    },
    "episodes": {
      "season_max_range": 100,
      "episode_max_range": 100,
      "max_range_gap": 1,
      "season_markers": [
        "s"
      ],
      "season_ep_markers": [
        "x"
      ],
      "disc_markers": [
        "d"
      ],
      "episode_markers": [
        "xe",
        "ex",
        "ep",
        "e",
        "x"
      ],
      "range_separators": [
        "-",
        "~",
        "to",
        "a"
      ],
      "discrete_separators": [
        "+",
        "&",
        "and",
        "et"
      ],
      "season_words": [
        "season",
        "saison",
        "seizoen",
        "serie",
        "seasons",
        "saisons",
        "series",
        "tem",
        "temp",
        "temporada",
        "temporadas",
        "stagione"
      ],
      "episode_words": [
        "episode",
        "episodes",
        "eps",
        "ep",
        "episodio",
        "episodios",
        "capitulo",
        "capitulos"
      ],
      "of_words": [
        "of",
        "sur"
      ],
      "all_words": [
        "All"
      ]
    },
    "language": {
      "synonyms": {
        "ell": [
          "gr",
          "greek"
        ],
        "spa": [
          "esp",
          "español",
          "espanol"
        ],
        "fra": [
          "français",
          "vf",
          "vff",
          "vfi",
          "vfq"
        ],
        "swe": [
          "se"
        ],
        "por_BR": [
          "po",
          "pb",
          "pob",
          "ptbr",
          "br",
          "brazilian"
        ],
        "deu_CH": [
          "swissgerman",
          "swiss german"
        ],
        "nld_BE": [
          "flemish"
        ],
        "cat": [
          "català",
          "castellano",
          "espanol castellano",
          "español castellano"
        ],
        "ces": [
          "cz"
        ],
        "ukr": [
          "ua"
        ],
        "zho": [
          "cn"
        ],
        "jpn": [
          "jp"
        ],
        "hrv": [
          "scr"
        ],
        "mul": [
          "multi",
          "dl"
        ]
      },
      "subtitle_affixes": [
        "sub",
        "subs",
        "esub",
        "esubs",
        "subbed",
        "custom subbed",
        "custom subs",
        "custom sub",
        "customsubbed",
        "customsubs",
        "customsub",
        "soft subtitles",
        "soft subs"
      ],
      "subtitle_prefixes": [
        "st",
        "v",
        "vost",
        "subforced",
        "fansub",
        "hardsub",
        "legenda",
        "legendas",
        "legendado",
        "subtitulado",
        "soft",
        "subtitles"
      ],
      "subtitle_suffixes": [
        "subforced",
        "fansub",
        "hardsub"
      ],
      "language_affixes": [
        "dublado",
        "dubbed",
        "dub"
      ],
      "language_prefixes": [
        "true"
      ],
      "language_suffixes": [
        "audio"
      ],
      "weak_affixes": [
        "v",
        "audio",
        "true"
      ]
    },
    "part": {
      "prefixes": [
        "pt",
        "part"
      ]
    },
    "release_group": {
      "forbidden_names": [
        "rip",
        "by",
        "for",
        "par",
        "pour",
        "bonus"
      ],
      "ignored_seps": "[]{}()"
    },
    "screen_size": {
      "frame_rates": [
        "23.976",
        "24",
        "25",
        "30",
        "48",
        "50",
        "60",
        "120"
      ],
      "min_ar": 1.333,
      "max_ar": 1.898,
      "interlaced": [
        "360",
        "480",
        "576",
        "900",
        "1080"
      ],
      "progressive": [
        "360",
        "480",
        "576",
        "900",
        "1080",
        "368",
        "720",
        "1440",
        "2160",
        "4320"
      ]
    },
    "website": {
      "safe_tlds": [
        "com",
        "org",
        "net"
      ],
      "safe_subdomains": [
        "www"
      ],
      "safe_prefixes": [
        "co",
        "com",
        "org",
        "net"
      ],
      "prefixes": [
        "from"
      ]
    }
  }


Backwards Compatibility
-----------------------
This is an advanced feature which exposes Guessit internal parameters. These parameters are exposed to help you
tweak Guessit results to fit your needs. We're willing to keep it backwards compatible, but in order to enhance Guessit,
these parameters might change without prior notice.
