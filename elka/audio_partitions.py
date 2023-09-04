"""
Scripts for retrieving links of the audio partitions form the following
repositories:
    - MusicBrainz
    - AcousticBrainz
    - Last.fm
    - Discogs
    - DBPedia
    - WikiData
    - YouTube

Notes for the alignment:
- Isophonics: has metadata and release, stored as audio_reference;
- JAAH: contains MusicBrainz IDs;
- CASD: already contains YouTube links;
- Schubert-Winterreise: contains musicbrainz IDs;
- Billboard: metadata incomplete, which can be retrieved from the full database
    dump (audio_references). From that, the YouTube links can be retrieved.
    Moreover, the spotify ID is available in the billboard_full_features.xlsx
    file.
- Robbie Williams: has release name;
- Uspop2002: has release name and track number;
- RWC-Pop: contacted the curator, awaiting response;
- Weimar Jazz Database: contains MusicBrainz IDs.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import tqdm

from elka import utils

import musicbrainzngs

musicbrainzngs.set_useragent("application", "0.01", "http://example.com")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



