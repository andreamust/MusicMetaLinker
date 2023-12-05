"""
Script for creating links between MusicBrainz given the extracted information
from the JAMS files.
"""

import musicbrainzngs as mb


class MusicBrainzAlign:
    """
    A class for linking music metadata to MusicBrainz database.

    Args:
        mbid_track (str): The MusicBrainz ID of the track.
        mbid_release (str): The MusicBrainz ID of the release.
        artist (str): The name of the artist.
        album (str): The name of the album.
        track (str): The name of the track.
        track_number (int): The track number.
        duration (float): The duration of the track.
        isrc (str): The ISRC of the track.
        strict (bool): Whether to use strict matching or not.

    Attributes:
        mbid (str): The MusicBrainz ID of the track.
        artist (str): The name of the artist.
        album (str): The name of the album.
        track (str): The name of the track.
        track_number (int): The track number.
        duration (float): The duration of the track.
        isrc (str): The ISRC of the track.
        strict (bool): Whether to use strict matching or not.
        limit (int): Whether to limit the search to a smaller set of candidates for faster querying.
    """

    def __init__(
            self,
            mbid_track: str | None = None,
            mbid_release: str | None = None,
            artist: str | None = None,
            album: str | None = None,
            track: str | None = None,
            track_number: int | None = None,
            duration: float | None = None,
            isrc: list | str | None = None,
            strict: bool = False,
            limit: int | None = None
            ):
        
        self.mbid_track = mbid_track
        self.mbid_release = mbid_release
        self.artist = artist
        self.album = album
        self.track = track
        self.track_number = track_number
        self.duration = duration * 1000 if isinstance(duration, float) else duration
        self.isrc = isrc
        if isinstance(self.isrc, str):
            self.isrc = [self.isrc]
        self.strict = strict
        self.limit = limit

        mb.set_useragent("elka", "0.1", "https://elka.com")

        self.best_match = self.get_best_match

    def _search_by_isrc(self) -> dict | None:
        """
        Searches for the track in the MusicBrainz database by ISRC code.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        if self.isrc:
            for isrc in self.isrc:
                try:
                    isrc_result = mb.get_recordings_by_isrc(
                        isrc=isrc,
                        includes=["artists", "releases", "isrcs"],
                        release_status=["official"]
                    )
                    return isrc_result
                except mb.ResponseError:
                    return None

    def _search_by_mbid(self) -> dict | None:
        """
        Searches for the track in the MusicBrainz database by MBID.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        try:
            mbid_results = mb.get_recording_by_id(
                id=self.mbid_track,
                includes=["artists", "releases", "isrcs", "discids", "url-rels"],
                release_status=["official"],
                release_type=["album", "ep", "single"],
            )
            return mbid_results
        except mb.ResponseError:
            return None

    def _get_track_mbid_from_release(self) -> str | None:
        """
        Searches for the track in the MusicBrainz database by MBID.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        # check if the id is a link, in case 
        mbid_results = mb.search_recordings(
            recording=self.track,
            artist=self.artist,
            release=self.album,
            dur=self.duration,
            tnum=self.track_number,
            strict=self.strict,
            rid=self.mbid_release,
        )
        
        if mbid_results['recording-list']:
            recordings = mbid_results["recording-list"]
            for recording in recordings:
                release_list_ids = [release["id"] for release in recording["release-list"]]
                if self.mbid_release in release_list_ids:
                    return recording["id"]
        return None

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
            limit=self.limit,
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

    def get_recording(self) -> dict | list | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : dict
            Dictionary containing the search results.
        """
        if self.mbid_release:
            self.mbid_track = self._get_track_mbid_from_release()
        if self.mbid_track:
            return self._search_by_mbid()
        elif self.isrc:
            return self._search_by_isrc()
        else:
            preliminary_results = self._search()
            return self._filter_search_results(preliminary_results)

    @property
    def get_best_match(self) -> dict | None:
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
            if "recording" in results.keys():
                return results["recording"]
        return None

    def get_track(self) -> str | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : str
            Dictionary containing the search results.
        """
        if self.best_match:
            return self.best_match.get("title", None)

    def get_artist(self) -> str | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : str
            Dictionary containing the search results.
        """
        if self.best_match:
            return self.best_match.get("artist-credit-phrase", None)

    def get_album(self) -> str | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : str
            Dictionary containing the search results.
        """
        try:
            return self.best_match["release-list"][0]["title"]  # type: ignore
        except (TypeError, KeyError):
            return None

    def get_duration(self) -> float | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : float
            Dictionary containing the search results.
        """
        try:
            return float(self.best_match["length"]) / 1000  # type: ignore
        except (TypeError, KeyError):
            return None

    def get_mbid(self) -> str | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        search_results : str
            Dictionary containing the search results.
        """
        if self.best_match:
            return self.best_match.get("id", None)
        
    def get_iswc(self) -> list[str] | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        iswc_list : list[str]
            Dictionary containing the search results.
        None
            If no ISWC code is found.
        """
        if self.best_match:
            return self.best_match.get("iswc-list", None)

    def get_isrc(self) -> list[str] | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        irsc_list : list[str]
            Dictionary containing the search results.
        None
            If no ISRC code is found.
        """
        if self.best_match:
            return self.best_match.get("isrc-list", None)

    def get_release_date(self) -> str | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        irsc_list : str
            Dictionary containing the search results.
        """
        try:
            return self.best_match["release-list"][0]["date"]  # type: ignore
        except (TypeError, KeyError):
            return None

    def get_track_number(self) -> int | None:
        """
        Searches for the track in the MusicBrainz database.
        Returns
        -------
        irsc_list : int
            Dictionary containing the search results.
        """
        try:
            return self.best_match["release-list"][0]["medium-list"][0][  # type: ignore
                "track-list"][0]["number"]
        except (TypeError, KeyError):
            return None


if __name__ == "__main__":
    # test the class

    mb_align = MusicBrainzAlign(
        #artist="Hanns-Udo Muller",
        album="",
        #track="Einsamkeit",
        track_number=None,
        duration=None,
        mbid_track=None,
        isrc='USMC161463279',
        #mbid_release="9e2fcbe4-e7f3-45c2-b24e-eb304f261fa9",
        strict=False,
    )
    search_results = mb_align.get_recording()
    print(mb_align.get_track())
    print(mb_align.get_artist())
    print(mb_align.get_album())
    print(mb_align.get_duration())
    print(mb_align.get_mbid())
    print(mb_align.get_isrc())
    print(mb_align.get_release_date())
    print(mb_align.get_track_number())
    print(mb_align.get_iswc())
