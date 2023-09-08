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

from linking import linking
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
    # iterate over the partitions
    for partition in partitions_path.iterdir():
        if partition.name == "isophonics":
            print(f"Processing partition {partition.name}")
            # open partition/choco/jams_converted if exists
            # else partition/choco/jams
            jams_converted = partition / "choco" / "jams_converted"
            if jams_converted.exists():
                jams_path = jams_converted
            else:
                jams_path = partition / "choco" / "jams"
            # iterate over the JAMS files
            for jams_file in jams_path.glob("*.jams"):
                print(f"Processing JAMS file {jams_file.name}")
                # process the JAMS file
                jams_process = JAMSProcessor(jams_file)
                # retrieve the links
                linker = linking.Align(
                    artist=jams_process.artist_name,
                    album=jams_process.album_name,
                    track=jams_process.track_name,
                    track_number=jams_process.track_number,
                    duration=jams_process.duration,
                    strict=True,
                )
                jams_process.track_name = linker.get_track()
                jams_process.artist_name = linker.get_artist()
                jams_process.album_name = linker.get_album()
                jams_process.track_number = linker.get_track_number()
                jams_process.duration = linker.get_duration()
                jams_process.release_year = linker.get_release_date()
                original_identifiers = jams_process.identifiers
                links = {}
                links['musicbrainz'] = linker.get_mbid()
                links['isrc'] = linker.get_isrc()
                links['deezer'] = linker.get_deezer_id()
                links['deezer_url'] = linker.get_deezer_link()

                # add the links to the identifiers
                jams_process.identifiers = {**original_identifiers, **links}

                if save:
                    save_path = jams_path.parents[1] / "jams_aligned"
                    jams_process.write_jams(save_path)


if __name__ == "__main__":
    retrieve_links(Path("../partitions"))
