"""
Scripts for retrieving the ISRC code from a Spotify ID.
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import mml_secrets as constants

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

os.environ['SPOTIPY_CLIENT_ID'] = constants.SPOTIFY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = constants.SPOTIFY_CLIENT_SECRET


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
        return track["external_ids"]["isrc"]  # type: ignore
    except spotipy.exceptions.SpotifyException:
        return None


if __name__ == "__main__":
    print(get_isrc("6y0igZArWVi6Iz0rj35c1Y"))
