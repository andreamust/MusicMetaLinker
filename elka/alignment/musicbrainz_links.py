"""
Script for creating links between MusicBrainz given the extracted information
from the JAMS files.
"""

import musicbrainzngs as mb


class MusiBrainzAlign:
    """
    Class for creating links between MusicBrainz given the extracted information
    from the JAMS files.
    """

    def __init__(
        self,
        artist: str = None,
        album: str = None,
        track: str = None,
        track_number: int = None,
        duration: float = None,
        strict: bool = False,
    ):
        """
        Initializes the class by taking the metadata of the track and the
        parameters for the search.
        Parameters
        ----------
        artist : str
            Artist name.
        album : str
            Album name.
        track : str
            Track name.
        track_number : int
            Track number.
        duration : float
            Track duration.
        strict : bool
            Whether to use strict search or not.
        Returns
        -------
        None
        """
        self.artist = artist
        self.album = album
        self.track = track
        self.track_number = track_number
        self.duration = duration
        self.strict = strict

        mb.set_useragent(
            "elka", "0.1", "https://elka.com")




