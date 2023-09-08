"""
Script for creating links between MusicBrainz given the extracted information
from the JAMS files.
"""

import musicbrainzngs as mb


class MusicBrainzAlign:
    """
    Class for creating links between MusicBrainz given the extracted information
    from the JAMS files.
    """

    def __init__(
        self,
        mbid: str = None,
        artist: str = None,
        album: str = None,
        track: str = None,
        track_number: int = None,
        duration: float = None,
        isrc: str = None,
        strict: bool = False,
    ):
        """
        Initializes the class by taking the metadata of the track and the
        parameters for the search.
        Parameters
        ----------
        mbid : str
            MusicBrainz ID.
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
        isrc : str
            ISRC code.
        strict : bool
            Whether to use strict search or not.
        Returns
        -------
        None
        """
        self.mbid = mbid
        self.artist = artist
        self.album = album
        self.track = track
        self.track_number = track_number
        self.duration = duration
        self.isrc = isrc
        self.strict = strict

        mb.set_useragent("elka", "0.1", "https://elka.com")

    def _search_by_isrc(self) -> dict:
        """
        Searches for the track in the MusicBrainz database by ISRC code.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        isrc_result = mb.get_recordings_by_isrc(
            isrc=self.isrc,
            includes=["artists", "releases", "isrcs", "discids", "url-rels"],
            release_status=["official"],
        )
        return isrc_result

    def _search_by_mbid(self) -> dict:
        """
        Searches for the track in the MusicBrainz database by MBID.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        mbid_results = mb.get_recording_by_id(
            id=self.mbid,
            includes=["artists", "releases", "isrcs", "discids", "url-rels"],
            release_status=["official"],
        )
        return mbid_results

    def _search(self):
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        search_results = mb.search_recordings(
            recording=self.track,
            artist=self.artist,
            release=self.album,
            dur=self.duration,
            tnum=self.track_number,
            strict=self.strict,
        )
        return search_results["recording-list"]

    @staticmethod
    def _filter_search_results(results: dict) -> list:
        """
        Filters the search results by length and track position. Moreover, it
        filters out results without a ISRC code.
        Parameters
        ----------
        results : dict
            Dictionary containing the search results.
        Returns
        -------
        search_results_filtered : dict
            Dictionary containing the filtered search results.
        """
        return [res for res in results if "isrc-list" in res.keys()]

    def get_recording(self):
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        if self.mbid:
            return self._search_by_mbid()
        elif self.isrc:
            return self._search_by_isrc()
        else:
            preliminary_results = self._search()
            return self._filter_search_results(preliminary_results)

    @property
    def get_best_match(self):
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        results = self.get_recording()
        if isinstance(results, list) and len(results) > 0:
            return results[0]
        elif isinstance(results, dict):
            return results["recording"]
        return None

    def get_track(self):
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        return self.get_best_match["title"]

    def get_artist(self):
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        return self.get_best_match["artist-credit-phrase"]

    def get_album(self):
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        return self.get_best_match["release-list"][0]["title"]

    def get_duration(self):
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        return int(self.get_best_match["length"]) / 1000

    def get_mbid(self):
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        return self.get_best_match["id"]

    def get_isrc(self) -> list[str] | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        irsc_list : list
            Dictionary containing the search results.
        None
            If no ISRC code is found.
        """
        try:
            return self.get_best_match["isrc-list"]
        except KeyError:
            return None

    def get_release_date(self) -> str:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        irsc_list : list
            Dictionary containing the search results.
        """
        return self.get_best_match["release-list"][0]["date"]


if __name__ == "__main__":
    # test the class

    mb_align = MusicBrainzAlign(
        artist="Louis Armstrong and His Hot Five",
        album="",
        track="Hotter Than That",
        track_number=None,
        duration=181.49,
        mbid="5478f78d-3cbc-4940-ab18-c605dd67b236",
        strict=True,
    )
    search_results = mb_align.get_recording()
    print(mb_align.get_best_match)
    print(mb_align.get_track())
    print(mb_align.get_artist())
    print(mb_align.get_album())
    print(mb_align.get_duration())
    print(mb_align.get_mbid())
    print(mb_align.get_isrc())
    print(mb_align.get_release_date())
