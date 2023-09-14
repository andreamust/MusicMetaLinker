"""
Scripts for retrieving links of the audio partitions form the following
repositories:
    - MusicBrainz
    - Deezer
    - YouTube Music
    - AcouticBrainz

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
- RWC-Pop: available at MTG;
- Weimar Jazz Database: contains MusicBrainz IDs.
"""

from pathlib import Path

import pandas as pd

from clean_partitions import clean_billboard
from linking import linking
from partitions_map import AUDIO_PARTITIONS, SCORE_PARTITIONS
from preprocessor import JAMSProcessor
from utils import log_downloaded_data


def complement_jams(linker: linking.Align,
                    jams_process: JAMSProcessor) -> None:
    """
    Complements the JAMS file with the retrieved links.
    Parameters
    ----------
    linker : linking.Align
        Linker object.
    jams_process : JAMSProcessor
        JAMSProcessor object.
    Returns
    -------
    None
    """
    pass


def retrieve_links_audio(partitions_path: Path,
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
        if partition.name not in AUDIO_PARTITIONS:
            continue
        print(f"Processing partition {partition.name}")
        # initialize data to be stored in a dataframe
        df_list = []

        # partition/choco/jams_converted if exists else partition/choco/jams
        jams_converted = partition / "choco" / "jams-converted"
        if jams_converted.exists():
            jams_path = jams_converted
        elif partition.name == "schubert-winterreise":
            jams_path = partition / "choco" / "audio" / "jams-converted"
        else:
            jams_path = partition / "choco" / "jams"
        # iterate over the JAMS files
        for jams_file in jams_path.glob("*.jams"):
            print(f"Processing JAMS file {jams_file.name}")
            # process the JAMS file
            jams_process = JAMSProcessor(jams_file)

            isrc, spotify_id = None, None
            # if partition is billboard, retrieve missing metadata
            if partition.name == "billboard":
                track_title = jams_process.track_name
                artist_name = jams_process.artist_name
                spotify_id, isrc = clean_billboard.clean_billboard(track_title,
                                                                   artist_name)
            # retrieve the links
            linker = linking.Align(
                artist=jams_process.artist_name,
                album=jams_process.album_name,
                track=jams_process.track_name,
                track_number=jams_process.track_number,
                duration=jams_process.duration,
                strict=False,
            )
            track_name = linker.get_track()
            artist_name = linker.get_artist()
            album_name = linker.get_album()
            track_number = linker.get_track_number()
            duration = linker.get_duration()
            release_year = linker.get_release_date()
            # get the identifiers
            original_identifiers = jams_process.identifiers
            links = {'musicbrainz': linker.get_mbid(),
                     'acousticbrainz': linker.get_acousticbrainz_link(),
                     'isrc': linker.get_isrc() if isrc is None else isrc,
                     'deezer_id': linker.get_deezer_id(),
                     'deezer': linker.get_deezer_link(),
                     'youtube': linker.get_youtube_link(),
                     'spotify_id': spotify_id,
                     }

            # add retrieved information to the JAMS file
            jams_process.track_name = track_name
            jams_process.artist_name = artist_name
            jams_process.album_name = album_name
            jams_process.track_number = track_number
            jams_process.duration = duration
            jams_process.release_year = release_year
            jams_process.identifiers = {**original_identifiers, **links}

            # store information in a dataframe
            df_list.append({'jams_file': jams_file.name,
                            'track_name': track_name,
                            'artist_name': artist_name,
                            'album_name': album_name,
                            'track_number': track_number,
                            'duration': duration,
                            'release_year': release_year,
                            'musicbrainz': links['musicbrainz'],
                            'isrc': links['isrc'],
                            'deezer_id': links['deezer'],
                            'deezer_url': links['deezer_url'],
                            'youtube_url': links['youtube_url'],
                            'acousticbrainz': links['acousticbrainz'],
                            })

            if save:
                save_path = jams_path.parent / "jams_aligned"
                jams_process.write_jams(save_path)

        # save the dataframe
        df = pd.DataFrame(df_list, index=None)
        log_downloaded_data(df, partition / "choco" / "linking.csv")


def retrieve_links_score(partitions_path: Path,
                         save: bool = True,
                         download: bool = False) -> None:
    """
    Retrieves the links for the score partitions.
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
        if partition.name not in SCORE_PARTITIONS:
            continue
        print(f"Processing partition {partition.name}")
        # initialize data to be stored in a dataframe
        df_list = []

        # partition/choco/jams_converted if exists else partition/choco/jams
        jams_converted = partition / "choco" / "jams-converted"
        if jams_converted.exists():
            jams_path = jams_converted
        else:
            jams_path = partition / "choco" / "jams"
        if partition.name == "ireal-pro":
            jams_path = partition / "choco" / "playlist" / "jams-converted"
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
                strict=False,
            )
            track_name = linker.get_track()
            artist_name = linker.get_artist()
            album_name = linker.get_album()
            track_number = linker.get_track_number()
            duration = linker.get_duration()
            release_year = linker.get_release_date()
            # get the identifiers
            original_identifiers = jams_process.identifiers
            links = {'musicbrainz': linker.get_mbid(),
                     'isrc': linker.get_isrc(),
                     'deezer': linker.get_deezer_id(),
                     'deezer_url': linker.get_deezer_link(),
                     'youtube_url': linker.get_youtube_link(),
                     }

            # add retrieved information to the JAMS file
            jams_process.track_name = track_name
            jams_process.artist_name = artist_name
            jams_process.album_name = album_name
            jams_process.track_number = track_number
            jams_process.duration = duration
            jams_process.release_year = release_year
            jams_process.identifiers = {**original_identifiers, **links}

            # store information in a dataframe
            df_list.append({'jams_file': jams_file.name,
                            'track_name': track_name,
                            'artist_name': artist_name,
                            'album_name': album_name,
                            'track_number': track_number,
                            'duration': duration,
                            'release_year': release_year,
                            'musicbrainz': linker.get_mbid(),
                            'isrc': linker.get_isrc(),
                            'deezer_id': linker.get_deezer_id(),
                            'deezer_url': linker.get_deezer_link(),
                            'youtube_url': linker.get_youtube_link(),
                            'acousticbrainz': linker.get_acousticbrainz_link(),
                            })

            if save:
                save_path = jams_path.parent / "jams_aligned"
                jams_process.write_jams(save_path)


if __name__ == "__main__":
    # retrieve_links_audio(Path("../partitions"))
    retrieve_links_score(Path("../partitions"))