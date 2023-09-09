"""
Scripts for retrieving the ISRC code from a Spotify ID.
"""
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

os.environ['SPOTIPY_CLIENT_ID'] = "9a23546dfb4c44399cdc5487958290dd"
os.environ['SPOTIPY_CLIENT_SECRET'] = "ec82edf304b34434965137da5e4b7eea"


def get_isrc(spotify_id: str) -> str | None:
    """
    Returns the ISRC code from a Spotify ID.
    Parameters
    ----------
    spotify_id : str
        Spotify ID.
    Returns
    -------
    str
        ISRC code.
    """
    client_credentials_manager = SpotifyClientCredentials()

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    track = sp.track(str(spotify_id))
    try:
        return track["external_ids"]["isrc"]
    except spotipy.exceptions.SpotifyException:
        return None


if __name__ == "__main__":
    print(get_isrc("6y0igZArWVi6Iz0rj35c1Y"))
