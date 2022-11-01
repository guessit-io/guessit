Changelog
=======

<!--next-version-placeholder-->

## v3.5.0 (2022-11-01)
### Feature
* **dependencies:** Drop Python 3.6 support ([`47f5718`](https://github.com/guessit-io/guessit/commit/47f57184a9d0a25c1b415638d0b003dad88ce607))

### Fix
* **audio_codec:** Detect "E-AC-3" and "AC-3" ([`72dc12e`](https://github.com/guessit-io/guessit/commit/72dc12e2489d240839a216041ffe47e9dd128b0f))
* **typo:** Fix common typo ([`42a80f0`](https://github.com/guessit-io/guessit/commit/42a80f0992387c96fc120480aaea35e4b3d9f5b8))

## v3.4.3 (2021-11-20)
### Fix
* **setuptools:** Drop usage of test_requires and setup_requires ([#720](https://github.com/guessit-io/guessit/issues/720)) ([`324b38c`](https://github.com/guessit-io/guessit/commit/324b38ce62cd43efc51074dbd8c5e2ed64fc7573))

## v3.4.2 (2021-11-08)
### Fix
* **dependencies:** Use babelfish>=0.6.0 ([#711](https://github.com/guessit-io/guessit/issues/711)) ([`d2c1b01`](https://github.com/guessit-io/guessit/commit/d2c1b010ed0025d62322e681471abe948c923a1d))

## v3.4.1 (2021-11-05)
### Fix
* **other:** Detect "Open Matte" with non-space separator ([`b52a9d9`](https://github.com/guessit-io/guessit/commit/b52a9d9f0315af68d41c22772d35488d00c4f04e))
* **packaging:** Use stdlib importlib.resources in py 3.7+ ([`1e7b000`](https://github.com/guessit-io/guessit/commit/1e7b0008232e306478d15f7a78d093804d56df3a))

## v3.4.0 (2021-11-04)
### Feature
* **other:** Add restored support and match 4k-* patterns ([`99c30eb`](https://github.com/guessit-io/guessit/commit/99c30eb3876a4947ff9a4f5126b70195452a64c7))
* **other:** Add 2in1 support ([`0cf07f4`](https://github.com/guessit-io/guessit/commit/0cf07f47559e0061a6df8437510e98e6afe69747))
* **python:** Add python 3.10 support, drop python 3.5 support ([`a8ea88d`](https://github.com/guessit-io/guessit/commit/a8ea88de31dcf642434fa4ab1315df2467a443ca))
* **audio_channels:** Add support for "1.0" audio channels ([`f22e33d`](https://github.com/guessit-io/guessit/commit/f22e33daada06956c085a5784387e5a4527417e6))
* **streaming_service:** Add more streaming services ([`40ce483`](https://github.com/guessit-io/guessit/commit/40ce4831600f915a91cea1e6aba4bcb4cfbc35f0))
* **other:** Add ONA/OAD support ([`0823e37`](https://github.com/guessit-io/guessit/commit/0823e37b382ed3470924a11a5024c0a9a383df30))
* **other:** Add Repack and ReRip followed by a digit support ([#653](https://github.com/guessit-io/guessit/issues/653)) ([`997c5c2`](https://github.com/guessit-io/guessit/commit/997c5c29f4adedcd7568a22b38155e2a8c83bf10))

### Fix
* **source:** Avoid Shots to be guessed as Showtime and TS ([`de85403`](https://github.com/guessit-io/guessit/commit/de85403dd40b120a3dc52f26960986a2fb482e64))
* **screen_size:** Add 540i ([`1a7db40`](https://github.com/guessit-io/guessit/commit/1a7db40a1f7d06f49db2ac116a1de074049334c0))
* **language:** Fix `language` and `subtitle_languages` in some situations ([#696](https://github.com/guessit-io/guessit/issues/696)) ([`f19cfda`](https://github.com/guessit-io/guessit/commit/f19cfda856958c4aa81dde36ecbb3df66cdd4b48))
* **packaging:** Use importlib-resources instead of pkgutil ([`a679a6c`](https://github.com/guessit-io/guessit/commit/a679a6c2b05607029a1267b0b217c5696f85df5f))
* **other:** Fix Open Matte when written as is ([#689](https://github.com/guessit-io/guessit/issues/689)) ([`ddf8e77`](https://github.com/guessit-io/guessit/commit/ddf8e772d735bc80940ba3068c5014d79499a618))
* **frame_rate:** Enhance `frame_rate` when ending with `.000` or space separated ([#693](https://github.com/guessit-io/guessit/issues/693)) ([`dba9cef`](https://github.com/guessit-io/guessit/commit/dba9cef859cb548988e411c2a9d537914da14f4e))
* **packaging:** Use importlib-resources instead of pkg_resources ([`6ef222e`](https://github.com/guessit-io/guessit/commit/6ef222ea2879343c7c3dd04dd081a2ce88a327aa))
* **edition:** Better support for "Criterion" ([`85ac52a`](https://github.com/guessit-io/guessit/commit/85ac52a771f53cc6e44bc48a0c3a017e971c0d71))
* **advanced-config:** Fix removal of custom rebulk rules ([#692](https://github.com/guessit-io/guessit/issues/692)) ([`c2bc1ea`](https://github.com/guessit-io/guessit/commit/c2bc1ea3809626442374f35d018b43e6c775758f))
* **streaming_service:** Make SBS ambiguous ([`777d2b5`](https://github.com/guessit-io/guessit/commit/777d2b56764d14431125cccb092978fa726c2453))
* **streaming_service:** Keep pattern to avoid rebuilding rules ([`62f0c0e`](https://github.com/guessit-io/guessit/commit/62f0c0ec5d43074175fffc2aff611b178ddb95a0))
* **proper_count:** Fix proper_count raw output to include all matches ([#626](https://github.com/guessit-io/guessit/issues/626)) ([`1faea7e`](https://github.com/guessit-io/guessit/commit/1faea7e9c8bc9ace9d343976ea1987a5f2628a4f))
* **website:** Fix website when it contains a digit ([#659](https://github.com/guessit-io/guessit/issues/659)) ([`9e39b7e`](https://github.com/guessit-io/guessit/commit/9e39b7e659e87dc3f71b1449a8994ef898212b0e))

### Documentation
* Add new properties ([`f1d8f61`](https://github.com/guessit-io/guessit/commit/f1d8f61fb6d326092e6caaf6419696e9419e8a73))

## v3.3.1 (2021-02-06)
### Fix
* **options:** Fix custom options.json groups starting/ending ([#671](https://github.com/guessit-io/guessit/issues/671)) ([`40f43b1`](https://github.com/guessit-io/guessit/commit/40f43b133cf5fb43d79c1e2b886a3620830a4a37))

### Documentation
* Lighten README and update doc index page ([`8e4ba6f`](https://github.com/guessit-io/guessit/commit/8e4ba6f0e4835026e85fca81faba267c95eb31fc))

## v3.3.0 (2021-02-03)
### Feature
* Add `--output-input-string` option ([#665](https://github.com/guessit-io/guessit/issues/665)) ([`bac6143`](https://github.com/guessit-io/guessit/commit/bac6143559d437edc34e2fde0b77172567e4451d))
* **streaming_service:** Add `Showtime`, `HBO` and `AppleTV` ([#661](https://github.com/guessit-io/guessit/issues/661)) ([`dc55eaa`](https://github.com/guessit-io/guessit/commit/dc55eaa6d0cdf9d5552c4dbaaa29c8df8365691c))
* **other:** Add `Hybrid` support ([#669](https://github.com/guessit-io/guessit/issues/669)) ([`522af53`](https://github.com/guessit-io/guessit/commit/522af5371cac467dd1f03abb08df9cbf5b409126))

### Fix
* **options:** Avoid appending `None` values to list when merging options ([#658](https://github.com/guessit-io/guessit/issues/658)) ([`42978c9`](https://github.com/guessit-io/guessit/commit/42978c909c4e5ebb2cc95b94583f80d73759f29a))
* **streaming_service:** Add iT keyword support for iTunes ([#669](https://github.com/guessit-io/guessit/issues/669)) ([`51e0021`](https://github.com/guessit-io/guessit/commit/51e00217947d8b993bcfb091b012da803245f698))
* **streaming_service:** Fix regex patterns declared with `re:` prefix ([`e02323f`](https://github.com/guessit-io/guessit/commit/e02323f6c1d1e74ef32dfbcfb3ab69e367d11a00))

### Documentation
* **readme:** Avoid mixed-content in github pages ([`2e1f29c`](https://github.com/guessit-io/guessit/commit/2e1f29ca47f8586930ca092b31f2431a1f3df52f))

## v3.2.0 (2020-12-23)
### Feature
* Add python 3.9 support, drop python 2.7 support ([`2c8b25e`](https://github.com/guessit-io/guessit/commit/2c8b25e77fb424d63f9f73318e85dd96cef865e0))

### Fix
* **regex:** Use rebulk 3+ to have regex module disabled by default ([`28658b2`](https://github.com/guessit-io/guessit/commit/28658b27720d9eb48c9f9f0edfadb3247910de43))

## 3.1.1 (2020-05-03)

-   Drop python 3.4 support
-   Use SafeLoader with yaml.load()

## 3.1.0 (2019-09-02)

-   Add python 3.8 support
-   Use rebulk 2.\*
-   Remove v from subtitle\_language prefix in default configuration
-   Add Variable Frame Rate value to other property (VFR tag)
-   Use episode words defined in configuration in a rebulk rule
-   Avoid trigger of useless rules consequences
-   Fix possible crash in weak episode removal
-   Fix issue caused by streaming\_service property conflicts
-   Fix source validation when more than one pattern match
-   Fix issue with some titles on multiple fileparts
-   Fix issue related to website exclusion inside title

## 3.0.4 (2019-06-04)

-   screen\_size property 540p was added.
-   Fix audio\_channel detection for 6.0
-   Fix common words being detected as language
-   streaming\_service is now configurable in advanced options
-   Add DC Universe to streaming\_service
-   Improve detection when release name in between brackets
-   Improve language detection
-   Fix wrong 3D detection
-   Fix to keep separators for single characters. E.g.: S.W.A.T.
-   Fix Show Name/Season SS/Ep. EE - Title
-   Added This is Us to default expected titles
-   Added suggested\_expected to the api to support apps that uses guessit as a library
-   Added Extras detection as other property
-   Add more streaming sites

## 3.0.3 (2018-10-23)

-   Add MP2 audio\_codec value.
-   Proper and Fix have been separated in two distinct other values.
-   Add 1e18 season/episode pattern.
-   Fix false release\_group matches with --expected-title option.
-   Fix parent folder ending with a digit detected as title
-   Fix wrong season/year with --type episode option. Serie(s) keyword has been removed from default configuration.
-   Fix missing property when episode\_details pattern appears in title.

## 3.0.2 (2018-10-18)

-   Ensure consistent behavior between CLI and Python module. It's now possible to override advanced\_config at runtime through options dict. Rebulk rules are lazily rebuilt when advanced\_config is changed since previous call.
-   Refactored command line options and loading behavior related to configuration files (see -c CONFIG, --config CONFIG, --no-user-config, --no-default-config)

## 3.0.1 (2018-10-17)

-   Removed Extras and Bonus values from episode\_details property as those tags may also appear in movies
-   Add Scalable Video Coding, Advanced Video Codec High Definition and High Efficiency Video Coding values to video\_profile
-   Add support for Python 3.7
-   Add mk3d value to container
-   Better title cleanup containing acronyms (like Marvel's Agents of S.H.I.E.L.D)
-   Fix issue with ES audio\_profile breaking titles
-   Fix crash for files ending with Rip

## 3.0.0 (2018-05-22)

-   Renamed format property to source.
-   source property Cam is now Camera or HD Camera
-   source property Telesync is now Telesync or HD Telesync
-   source property PPV is now Pay-per-view
-   source property DVB is now Digital TV
-   source property VOD is now Video on Demand
-   source property WEBRip is now Web with additional property \`other\`: Rip
-   source property WEB-DL is now Web
-   source property AHDTV is now Analog HDTV
-   source property UHDTV is now Ultra HDTV
-   source property HDTC is now HD Telecine
-   screen\_size property 360i was added.
-   screen\_size property 480i was added.
-   screen\_size property 576i was added.
-   screen\_size property 900i was added.
-   screen\_size property 1440p was added.
-   screen\_size property 4K is now 2160p
-   screen\_size property 4320p was added.
-   video\_codec property h264 is now H.264
-   video\_codec property h265 is now H.265
-   video\_codec property Mpeg2 is now MPEG-2
-   video\_codec property Real is now RealVideo
-   video\_codec property XviD is now Xvid
-   video\_profile property BP is now Baseline.
-   video\_profile property HP is now High.
-   video\_profile property XP is now Extended.
-   video\_profile property MP is now Main.
-   video\_profile property Hi422P is now High 4:2:2.
-   video\_profile property Hi444PP is now High 4:4:4 Predictive.
-   video\_profile property High 10 was added.
-   video\_profile property 8bit was removed. 8bit is detected as \`color\_depth\`: 8-bit
-   video\_profile property 10bit was removed. 10bit is detected as \`color\_depth\`: 10-bit
-   audio\_codec property DTS-HD was added.
-   audio\_codec property AC3 is now Dolby Digital
-   audio\_codec property EAC3 is now Dolby Digital Plus
-   audio\_codec property TrueHD is now Dolby TrueHD
-   audio\_codec property DolbyAtmos is now Dolby Atmos.
-   audio\_profile property HE is now High Efficiency.
-   audio\_profile property LC is now Low Complexity.
-   audio\_profile property HQ is now High Quality.
-   audio\_profile property HDMA is now Master Audio.
-   edition property Collector Edition is now Collector
-   edition property Special Edition is now Special
-   edition property Criterion Edition is now Criterion
-   edition property Deluxe Edition is now Deluxe
-   edition property Limited Edition is now Limited
-   edition property Theatrical Edition is now Theatrical
-   edition property Director's Definitive Cut was added.
-   episode\_details property Oav and Ova were removed. They are now other: Original Animated Video
-   episode\_details property Omake is now Extras
-   episode\_details property Final was added.
-   other property Rip was added.
-   other property DDC was removed. DDC is now \`edition\`: Director's Definitive Cut
-   other property CC was removed. CC is now \`edition\`: Criterion
-   other property FINAL was removed. FINAL is now \`episode\_details\`: Final
-   other property Original Animated Video was added.
-   other property OV is now Original Video
-   other property AudioFix is now Audio Fixed
-   other property SyncFix is now Sync Fixed
-   other property DualAudio is now Dual Audio
-   other property Fansub is now Fan Subtitled
-   other property Fastsub is now Fast Subtitled
-   other property FullHD is now Full HD
-   other property UltraHD is now Ultra HD
-   other property mHD and HDLight are now Micro HD
-   other property HQ is now High Quality
-   other property HR is now High Resolution
-   other property LD is now Line Dubbed
-   other property MD is now Mic Dubbed
-   other property Low Definition was added.
-   other property LiNE is now Line Audio
-   other property R5 is now Region 5
-   other property Region C was added.
-   other property ReEncoded is now Reencoded
-   other property WideScreen is now Widescreen
-   Added Ultra HD Blu-ray as new source possible value.
-   Added Standard Dynamic Range as new other possible value.
-   Added HDR10 as new other possible value.
-   Added Dolby Vision as new other possible value.
-   Added BT.2020 as new other possible value.
-   Added 12-bit as new color\_depth possible value.
-   Added IMAX as new edition possible value.
-   Added Upscaled as new other possible value.
-   Added High Frame Rate as new other possible value.
-   Added Ultimate as new edition possible value.
-   Added Fan as new edition possible value.
-   Added High Resolution Audio as new audio\_profile possible value.
-   Added Extended Surround as new audio\_profile possible value.
-   Added EX as new audio\_profile possible value
-   Added Opus as new audio\_codec possible value
-   Added aspect\_ratio as new property. Also used to validate if a screen\_size is a standard resolution.
-   Fixed unwanted language and country detection for exotic languages.
-   Added default and configurable list of allowed languages and countries
-   Added VC-1 as new video\_codec possible value
-   Enhanced dash-separated release\_group detection.
-   Changed size output to return guessit.Quantity object.
-   Changed size output to return guessit.Size object.
-   Added audio\_video\_rate as new possible property.
-   Added video\_video\_rate as new possible property.
-   Added frame\_rate as new possible property.
-   Added disc as a new possible property.
-   Added H.263 as new video\_codec possible value.
-   Added VP7 as new video\_codec possible value.
-   Added VP8 as new video\_codec possible value.
-   Added VP9 as new video\_codec possible value.
-   Added Vorbis as new audio\_codec possible value.
-   Added PCM as new audio\_codec possible value.
-   Added LPCM as new audio\_codec possible value.
-   Added Digital Master as new source possible value.
-   Added several new values for streaming\_service.
-   Added new options --includes and --excludes.
-   Added Sample as new other possible value.
-   Added Obfuscated as new other possible value.
-   Added Proof as new other possible value.
-   Added Repost as new other possible value.
-   Added advanced guessit configuration to config files.
-   Add support for pathlib.Path objects on guessit API input.

## 2.1.4 (2017-06-01)

-   Fix broken match function when using rebulk\>=0.9.0.

## 2.1.3 (2017-05-31)

-   Add nzb as new container possible value
-   Add EAC3 as new audio\_codec possible value
-   Add FullHD as new other possible value
-   Added python 3.6 support
-   Dropped python 2.6 support
-   Make container values consistent and always lowercase
-   Fix --type movie being ignored for movies that starts with numbers
-   Fix invalid language detection due the common words audio, true and unknown
-   Fix episode type detection when series name contains year followed by SEE pattern

## 2.1.2 (2017-04-03)

-   Many fixes, additions and improvements (thanks to @ratoaq2).

## 2.1.1 (2016-12-04)

-   Add \~ to episode/season separators.
-   Add AHDTV, HDTC, SATRip as new format possible values.
-   Add streaming\_service property.
-   Add DDP pattern as audio\_codec=\`DolbyDigital\`.
-   Add LDTV as possible tag for other=\`LD\`.
-   Add StripSeparators Post Processor to strip separators from all matches.
-   Fix invalid guess 1 x 2 with --type episode.
-   Fix part property.
-   Fix cd\_count issue with x264-CD.
-   Fix HDD group detected as DolbyDigital.
-   Fix invalid comparator in audio\_codec conflict solver.
-   Fix validation of film property.
-   Fix date followed by screen\_size invalid guess.
-   Fix episode not detected when smaller filepart repeats the season and uses SSEE pattern.
-   Enhance season/episode conflict solver to keep most specific value.
-   Enhance video\_profile detection.
-   Enhance episode/season range and sequence guessing.
-   Enhance performance with rebulk upgrade to 0.8.2.
-   Enhance season/episode.
-   Enhance other=\`Complete\` guessing.
-   Enhance release\_group guessing.
-   Enhance command line options parsing related to unicode.
-   Ensure roman numbers are surrounded with separators to be guessed as numbers.

## 2.1.0 (2016-09-08)

-   Drop support for regex native module.
-   Remove dependency constraint on python-dateutil.
-   Enhance langage/country guessing in edge cases.
-   Enhance rule to guess release\_group in more file templates.
-   Fix edge cases for subtitle language detection.
-   Fix invalid conflict solving in season/episode occuring between SssEee and ssXee pattern.
-   Fix issue when running guessit in non-interactive shell with python 2
-   Guess Dolby keyword as DolbyDigital in audio\_codec.
-   Avoid title to be guessed as website (Dark.Net)
-   Avoid season/episode to be guessed when pattern is included inside words.
-   Enhance screen\_size to detect 720pHD and 1080pHD
-   Add support for format and video\_codec when no separators between themselves. (HDTVx264, PDTVx264, ...)
-   Add rebulk version in --version option.
-   Upgrade rebulk to 0.7.3.

## 2.0.5 (2016-04-10)

-   Fix inconsistent properties returned by guessit -p.
-   Add support for titles containing dots.
-   Lock python-dateutil dependency to \<2.5.2.

## 2.0.4 (2016-02-03)

-   Add an Exception Report when an unexpected exception occurs.

## 2.0.3 (2016-01-30)

-   Something goes wrong with 2.0.2 release ...

## 2.0.2 (2016-01-30)

-   Fix possible issue with unicode characters encoding/decoding.
-   Pypy is now supported.

## 2.0.1 (2016-01-28)

-   Add support for any type of string with python 2 and python 3 (binary, str, unicode).

## 2.0.0 (2016-01-27)

-   Final release.

## 2.0rc8 (2016-01-26)

-   Remove regex native module from required dependencies. It will now be used only if present.

## 2.0rc7 (2016-01-18)

-   Fix packaging issues on Python 2.7.

## 2.0rc6 (2016-01-18)

-   Fix packaging issues.

## 2.0rc5 (2016-01-18)

-   Guessit is now available as a docker container on Docker Hub (<https://hub.docker.com/r/toilal/guessit>).
-   country 2-letter code is not added to title value anymore.
-   All container values are now capitalized.
-   alternativeTitle has been renamed to alternative\_title and added to the docs.
-   mimetype property is now in the docs.
-   Add more excluded words for language property.
-   Add more possible values for other property.
-   Fix an issue occuring with title values starting with Scr.
-   film property is now guessed only if less than 100 to avoid possible conflicts with crc32.

## 2.0rc4 (2015-12-03)

-   Add docs.
-   Add exotic screen\_size patterns support like 720hd and 720p50.
-   Rename audio\_codec value true-HD to trueHD.

## 2.0rc3 (2015-11-29)

-   Add \_\_version\_\_ to main module.

## 2.0rc2 (2015-11-28)

-   Single digit episodes are now guessed for --type episode instead of --episode-prefer-number.
-   Fix separators that could cause some titles to be splited with & and ;.
-   Avoid possible NoneType error.

## 2.0rc1 (2015-11-27)

-   Fallback to default title guessing when expected-title is not found.

## 2.0b4 (2015-11-24)

-   Add expected-group option.
-   Add validation rule for single digit episode to avoid false positives.
-   Add verbose option.
-   Fix expected-title option.
-   Better unicode support in expected-group/expected-title option.

## 2.0b3 (2015-11-15)

-   Add support for part with no space before number.
-   Avoid uuid and crc32 collision with season/episode properties.
-   Add better space support for season/episode properties.
-   Ensure date property is found when conflicting with season/episode properties.
-   Fix IndexError when input has a closing group character with no opening one before.
-   Add --type option.
-   Add rebulk implicit option support.

## 2.0b2 (2015-11-14)

-   Add python 2.6 support.

## 2.0b1 (2015-11-11)

-   Enhance title guessing.
-   Upgrade rebulk to 0.6.1.
-   Rename properCount to proper\_count
-   Avoid crash when using -p/-V option with --yaml and yaml module is not available.

## 2.0a4 (2015-11-09)

-   Add -p/-V options to display properties and values that can be guessed.

## 2.0a3 (2015-11-08)

-   Allow rebulk customization in API module.

## 2.0a2 (2015-11-07)

-   Raise TypeError instead of AssertionError when non text is given to guessit API.
-   Fix packaging issues with previous release blocking installation.

## 2.0a1 (2015-11-07)

-   Rewrite from scratch using Rebulk.
-   Read MIGRATION.rst for migration guidelines.
