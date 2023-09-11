"""
Module for alignment of tracks to the web resources.
So far, the web services implemented are:
    - MusicBrainz
    - Deezer
    - YouTube Music
"""

from .deezer_links import DeezerAlign
from .musicbrainz_links import MusicBrainzAlign
from .youtube_links import YouTubeAlign

__all__ = ["DeezerAlign", "MusicBrainzAlign", "YouTubeAlign"]
