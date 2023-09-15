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

import logging
import argparse
from pathlib import Path

import pandas as pd

from clean_partitions import clean_billboard
from filter_partitions import filter_partition
from linking import linking
from preprocessor import JAMSProcessor
from utils import log_downloaded_data

logger = logging.getLogger(__name__)


def complement_jams(linker: linking.Align,
                    jams_process: JAMSProcessor,
                    df_list: list,
                    jams_file: Path,
                    isrc: str = None,
                    spotify_id: str = None) -> list:
    """
    Complements the JAMS file with the retrieved links.
    Parameters
    ----------
    linker : linking.Align
        Linker object.
    jams_process : JAMSProcessor
        JAMSProcessor object.
    df_list : list
        List of dictionaries to be stored in a dataframe.
    jams_file : Path
        Path to the JAMS file.
    isrc : str
        ISRC code.
    spotify_id : str
        Spotify ID.
    Returns
    -------
    None
    """
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
             'deezer_url': linker.get_deezer_link(),
             'youtube_url': linker.get_youtube_link(),
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
                    'deezer_id': links['deezer_id'],
                    'deezer_url': links['deezer_url'],
                    'youtube_url': links['youtube_url'],
                    'acousticbrainz': links['acousticbrainz'],
                    'spotify_id': links['spotify_id'],
                    })

    return df_list


def retrieve_links(partitions_path: Path,
                   save: bool = True,
                   limit: str | None = None) -> None:
    """
    Iterates over the partitions and retrieves the links for each one of them.
    Parameters
    ----------
    partitions_path : Path
        Path to the partitions.
    save : bool
        Whether to save the retrieved information in a new JAMS file or not.
    limit : str | None
        Limit for the partition, accepts "audio", "score" or None.
    Returns
    -------
    None
    """
    # iterate over the partitions
    for partition in partitions_path.iterdir():
        # log partition information
        logger.info(f"Processing partition {partition.name}")
        # initialize data to be stored in a dataframe
        df_list = []
        # get the path to the JAMS files for the partition
        partition_type, jams_path = filter_partition(partition, limit=limit)
        if jams_path is None or partition_type is None:
            continue

        # iterate over the JAMS files
        for jams_file in jams_path.glob("*.jams"):
            # log track information
            logger.info(f"Processing JAMS file {jams_file.name}")
            # process the JAMS file
            jams_process = JAMSProcessor(jams_file)

            # get data from specific partitions
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
                duration=jams_process.duration if partition_type == "audio" else None,
                strict=False,
            )

            # complement the JAMS file with the retrieved links
            df_list = complement_jams(linker, jams_process, df_list, jams_file,
                                      isrc, spotify_id)

            if save:
                save_path = jams_path.parent / "jams_aligned"
                jams_process.write_jams(save_path)

        # save the dataframe
        df = pd.DataFrame(df_list, index=None)
        log_downloaded_data(df, partition / "choco" / "linking.csv")


def main():
    """
    Main function for retrieving the links.
    """
    parser = argparse.ArgumentParser(
        description="Retrieve links for the partitions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("partitions_path", type=Path,
                        help="Path to the partitions.")
    parser.add_argument("--save", action="store_true",
                        help="Whether to save the retrieved information in a "
                             "new JAMS file or not.")
    parser.add_argument("--limit", type=str, default=None,
                        help="Limit for the partition, accepts 'audio', "
                             "'score' or None.",
                        choices=["audio", "score"])
    args = parser.parse_args()

    retrieve_links(args.partitions_path, args.save, args.limit)


if __name__ == "__main__":
    main()