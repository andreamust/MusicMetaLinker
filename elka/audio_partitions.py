"""
Scripts for retrieving links of the audio partitions form the following
repositories:
    - MusicBrainz
    - Deezer

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

from pathlib import Path

from linking import deezer_links, musicbrainz_links
from preprocessor import JAMSProcessor

import glob
import os

def retrieve_links(partitions_path: Path,
                   save: bool = True,
                   download: bool = False):
    """
    Iterates over the partitions and retrieves the links for each one of them.
    Parameters
    ----------
    partitions_path : Path
        Path to the partitions.
    save : bool
        Whether to save the retrieved information in a new JAMS file or not.
    download : bool
        Whether to download the audio files or not.
    Returns
    -------
    None
    """


