"""
Cleans the billboard data set by retrieving missing metadata from the full
database dump.
"""

import pandas as pd

from elka.linking.spotify_links import get_isrc


def clean_billboard(track_title: str,
                    artist_name: str):
    """
    Cleans the billboard data set by retrieving missing metadata from the full
    database dump.
    Parameters
    ----------
    track_title : str
        Track title.
    artist_name : str
        Artist name.
    track_duration : float
        Track duration.
    Returns
    -------
    isrc : str
        ISRC code.
    spotify_id : str
        Spotify ID.
    """
    full_db = pd.read_excel("../audio_references/billboard_full_features.xlsx")
    # retrieve the track metadata
    track_metadata = full_db.loc[
        (full_db["Song"] == track_title) &
        (full_db["Performer"] == artist_name)
    ]

    # if no metadata is found, try to invert the artist and track title
    if track_metadata.empty:
        track_metadata = full_db.loc[
            (full_db["Song"] == artist_name) &
            (full_db["Performer"] == track_title)
        ]

    # get the spotify_track_id from the track_metadata
    spotify_id = track_metadata["spotify_track_id"].values[0]
    # get the isrc from the track_metadata
    try:
        isrc = get_isrc(spotify_id)
    except Exception:
        isrc = None

    return spotify_id, isrc


if __name__ == '__main__':
    # test the function
    track_title = "You Can't Judge A Book By The Cover"
    artist_name = "Bo Diddley"
    spotify_id, isrc = clean_billboard(track_title, artist_name)
    print(f"Spotify ID: {spotify_id}")
    print(f"ISRC: {isrc}")






