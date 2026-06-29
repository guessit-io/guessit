#!/usr/bin/env python
"""Schema mapping from external release-name parsers to the guessit vocabulary.

External parsers (PTT, scene-release-parser, PTN, go-ptn, anitomy, ...) each use
their own field names and value vocabularies. This module translates a single
external label dict into a guessit-flavoured ``expected`` dict, keeping ONLY the
fields whose semantics are unambiguous enough to assert against guessit.

Used by ``scripts/import_cross_parser_tests.py`` at import time; the produced
values are vendored as JSON so the suite itself never needs this module nor a
network.
"""

from __future__ import annotations

from typing import Any

# --- value normalisation tables (external token -> guessit vocabulary) --------

# guessit collapses many physical sources into a single value (verified against
# the real parser): BluRay/BDRip/BRRip -> "Blu-ray", WEB-DL/WEBRip -> "Web", ...
SOURCE_MAP: dict[str, str] = {
    "bluray": "Blu-ray",
    "blu-ray": "Blu-ray",
    "bdrip": "Blu-ray",
    "brrip": "Blu-ray",
    "bdmux": "Blu-ray",
    "bdremux": "Blu-ray",
    "uhd bluray": "Ultra HD Blu-ray",
    "uhd blu-ray": "Ultra HD Blu-ray",
    "web": "Web",
    "web-dl": "Web",
    "webdl": "Web",
    "webrip": "Web",
    "web-rip": "Web",
    "hdtv": "HDTV",
    "hdtvrip": "HDTV",
    "pdtv": "HDTV",
    "dsr": "Satellite",
    "dvb": "Digital TV",
    "dvd": "DVD",
    "dvdrip": "DVD",
    "dvdr": "DVD",
    "dvd-r": "DVD",
    "dvdscr": "Screener",
    "hddvd": "HD-DVD",
    "hd-dvd": "HD-DVD",
    "vhs": "VHS",
    "vhsrip": "VHS",
    "tv": "TV",
    "satrip": "Satellite",
    "cam": "Camera",
    "camrip": "Camera",
    "ts": "Telesync",
    "telesync": "Telesync",
    "tc": "Telecine",
    "telecine": "Telecine",
    "ppv": "Pay-per-view",
    "laserdisc": "Laserdisc",
    "workprint": "Workprint",
}

VIDEO_CODEC_MAP: dict[str, str] = {
    "avc": "H.264",
    "h264": "H.264",
    "h.264": "H.264",
    "x264": "H.264",
    "hevc": "H.265",
    "h265": "H.265",
    "h.265": "H.265",
    "x265": "H.265",
    "xvid": "Xvid",
    "divx": "DivX",
    "mpeg2": "MPEG-2",
    "mpeg-2": "MPEG-2",
    "vc1": "VC-1",
    "vc-1": "VC-1",
    "vp9": "VP9",
    "vp8": "VP8",
    "h263": "H.263",
    "h.263": "H.263",
}

AUDIO_CODEC_MAP: dict[str, str] = {
    "aac": "AAC",
    "dts": "DTS",
    "dts-hd": "DTS-HD",
    "dtshd": "DTS-HD",
    "dts:x": "DTS:X",
    "dts-x": "DTS:X",
    "truehd": "Dolby TrueHD",
    "dolby truehd": "Dolby TrueHD",
    "atmos": "Dolby Atmos",
    "dolby atmos": "Dolby Atmos",
    "ac3": "Dolby Digital",
    "dd": "Dolby Digital",
    "dolby digital": "Dolby Digital",
    "eac3": "Dolby Digital Plus",
    "ddp": "Dolby Digital Plus",
    "dd+": "Dolby Digital Plus",
    "dolby digital plus": "Dolby Digital Plus",
    "flac": "FLAC",
    "mp3": "MP3",
    "mp2": "MP2",
    "opus": "Opus",
    "pcm": "PCM",
    "lpcm": "LPCM",
    "vorbis": "Vorbis",
}


def _norm_token(value: Any) -> str:
    return str(value).strip().lower()


def map_source(value: Any) -> str | None:
    return SOURCE_MAP.get(_norm_token(value))


def map_video_codec(value: Any) -> str | None:
    return VIDEO_CODEC_MAP.get(_norm_token(value))


def map_audio_codec(value: Any) -> str | None:
    # external corpora sometimes give a list of audio terms; take the first known
    if isinstance(value, (list, tuple)):
        for item in value:
            mapped = AUDIO_CODEC_MAP.get(_norm_token(item))
            if mapped:
                return mapped
        return None
    return AUDIO_CODEC_MAP.get(_norm_token(value))


def map_screen_size(value: Any, known: set[str]) -> str | None:
    # guessit advertises both "<n>p"/"<n>i" and exact pixel sizes ("1280x720") in
    # its enum, so a token maps iff it is one of those advertised values.
    token = _norm_token(value).replace("×", "x")  # noqa: RUF001 (normalise multiplication sign)
    return token if token in known else None


def map_int(value: Any) -> int | None:
    try:
        if isinstance(value, bool):
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def map_season_episode(value: Any) -> int | list[int] | None:
    """Normalise PTT-style ``[5]`` / ``[1, 2]`` and bare ints to scalar-or-list."""
    if isinstance(value, (list, tuple)):
        nums = [n for n in (map_int(v) for v in value) if n is not None]
        if not nums:
            return None
        return nums[0] if len(nums) == 1 else nums
    return map_int(value)
