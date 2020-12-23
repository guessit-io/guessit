Migration
=========

Guessit 3 has introduced breaking changes from previous versions. You can find in this file all information required to perform a migration from previous version `2.x`.

API
---

No changes.

Properties
----------

Some properties have been renamed.

-   `format` is now `source`.

Values
------

The major changes in GuessIt 3 are around the values. Values were renamed in order to keep consistency and to be more intuitive. Acronyms are uppercase (e.g.: `HDTV`). Names follow the official name (e.g.: `Blu-ray`). Words have only the first letter capitalized (e.g.: `Camera`) except prepositions (e.g.: `on`) which are all lowercase.

The following values were changed:

### `source` (former `format` property)

-   `Cam` is now `Camera` or `HD Camera`
-   `Telesync` is now `Telesync` or `HD Telesync`
-   `PPV` is now `Pay-per-view`
-   `DVB` is now `Digital TV`
-   `VOD` is now `Video on Demand`
-   `WEBRip` is now `Web` with additional property `other: Rip`
-   `WEB-DL` is now `Web`
-   `AHDTV` is now `Analog HDTV`
-   `UHDTV` is now `Ultra HDTV`
-   `HDTC` is now `HD Telecine`

### `screen_size`

-   `360i` was added.
-   `480i` was added.
-   `576i` was added.
-   `900i` was added.
-   `4K` is now `2160p`
-   `4320p` was added.

### `video_codec`

-   `h264` is now `H.264`
-   `h265` is now `H.265`
-   `Mpeg2` is now `MPEG-2`
-   `Real` is now `RealVideo`
-   `XviD` is now `Xvid`

### `video_profile`

-   `BP` is now `Baseline`.
-   `HP` is now `High`.
-   `XP` is now `Extended`.
-   `MP` is now `Main`.
-   `Hi422P` is now `High 4:2:2`.
-   `Hi444PP` is now `High 4:4:4 Predictive`.
-   `High 10` was added.
-   `8bit` was removed. `8bit` is detected as `color_depth: 8-bit`
-   `10bit` was removed. `10bit` is detected as `color_depth: 10-bit`

### `audio_codec`

-   `DTS-HD` was added.
-   `AC3` is now `Dolby Digital`
-   `EAC3` is now `Dolby Digital Plus`
-   `TrueHD` is now `Dolby TrueHD`
-   `DolbyAtmos` is now `Dolby Atmos`.

### `audio_profile`

-   `HE` is now `High Efficiency`.
-   `LC` is now `Low Complexity`.
-   `HQ` is now `High Quality`.
-   `HDMA` is now `Master Audio`.

### `edition`

-   `Collector Edition` is now `Collector`
-   `Special Edition` is now `Special`
-   `Criterion Edition` is now `Criterion`
-   `Deluxe Edition` is now `Deluxe`
-   `Limited Edition` is now `Limited`
-   `Theatrical Edition` is now `Theatrical`
-   `Director's Definitive Cut` was added.

### `episode_details`

-   `Oav` and `Ova` were removed. They are now `other: Original Animated Video`
-   `Omake` is now `Extras`
-   `Final` was added.

### `other`

-   `Rip` was added. E.g.: `DVDRip` will output `other: Rip`
-   `DDC` was removed. `DDC` is now `edition: Director's Definitive Cut`
-   `CC` was removed. `CC` is now `edition: Criterion`
-   `FINAL` was removed. `FINAL` is now `episode_details: Final`
-   `Original Animated Video` was added.
-   `OV` is now `Original Video`
-   `AudioFix` is now `Audio Fixed`
-   `SyncFix` is now `Sync Fixed`
-   `DualAudio` is now `Dual Audio`
-   `Fansub` is now `Fan Subtitled`
-   `Fastsub` is now `Fast Subtitled`
-   `FullHD` is now `Full HD`
-   `UltraHD` is now `Ultra HD`
-   `mHD` and `HDLight` are now `Micro HD`
-   `HQ` is now `High Quality`
-   `HR` is now `High Resolution`
-   `LD` is now `Line Dubbed`
-   `MD` is now `Mic Dubbed`
-   `Low Definition` was added.
-   `LiNE` is now `Line Audio`
-   `R5` is now `Region 5`
-   `Region C` was added.
-   `ReEncoded` is now `Reencoded`
-   `WideScreen` is now `Widescreen`

