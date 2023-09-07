"""
Scripts for retrieving links of the audio partitions form the following
repositories:
    - MusicBrainz
    - Deezer

The scripts are based on the following libraries:
    - musicbrainzngs
    - deezer-python

The library will be expanded in the future to support more repositories, such
as Spotify, YouTube, etc.
"""

from .deezer_links import DeezerAlign

__all__ = ["DeezerAlign"]




