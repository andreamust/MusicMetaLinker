"""
Scripts for linking tracks to Deezer IDs using the Deezer API and their
search functionalities.
The script searches for correspondences in the Deezer database given the
title, artist and album of the track.
- If an ISRC is provided, the best match is the one with the same ISRC.
- If a duration is provided, the best match is the one with the closest
duration to the provided one.
- If a track number is provided, the best match is the one with the same
track number.
- Otherwise, the best match is the first result returned by
the Deezer API.
"""

import deezer


class DeezerAlign:
    """
    Search for a track on Deezer and return its data.
    """

    def __init__(
        self,
        artist: str | None = None,
        album: str | None = None,
        track: str | None = None,
        track_number: int | None = None,
        duration: float | None = None,
        isrc: str | list | None = None,
        strict: bool = False,
        fuzzy: bool = True,
    ):
        """
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
            Duration of the track in seconds.
        isrc : str | list
            ISRC identifiers of the track.
        strict : bool
            If True, raises an error if the input data do not correspond to any
            track on Deezer. If False, returns the best match.
            Default is False.
        fuzzy : bool
            If True, uses fuzzy matching to find the best match.
            Default is True.
        Raises
        ------
        ValueError
            If no parameters are passed.
        """
        self.artist = artist
        self.album = album
        if self.album and not strict and " " in self.album:
            self.album = " ".join(self.album.split(" ")[:2])
        self.track = track
        self.track_number = track_number
        self.duration = duration
        if isinstance(isrc, str):
            self.isrc = [isrc]
        self.isrc = isrc
        self.strict = strict
        self.fuzzy = False if fuzzy is True else True

        # connect to Deezer API
        self.deezer_client = deezer.Client()

    def _get_data(self, limit: int | None = None) -> list[deezer.Track] | None:   
        """
        Search for a track on Deezer and return its data.
        Parameters
        ----------
        limit : int
            Maximum number of results to return.
        Returns
        -------
        list[deezer.resources.Track]
            List of Track objects, each of which contains the data of a track.
        Raises
        ------
        ValueError
            If the track is not found.
        """
        results = self.deezer_client.search(
            track=self.track, artist=self.artist, album=self.album, strict=self.fuzzy,
        )

        if len(results) == 0:
            return None
        return [res for res in results][:limit]

    def _filter_duration(
        self, results: list[deezer.Track], duration_threshold: int
    ) -> list[deezer.Track]:
        """
        Filter results based on the duration of the track.
        Parameters
        ----------
        results : list[deezer.resources.Track]
            List of Track objects, each of which contains the data of a track.
        duration_threshold : int
            Threshold for the duration difference between the best match and
            the provided duration. If the difference is greater than the
            threshold, an error is raised.
        Returns
        -------
        list[deezer.resources.Track]
            List of Track objects, each of which contains the data of a track,
            filtered by duration. Only tracks with a duration within the
            threshold are returned.
        """
        if self.duration is None or self.strict is False:
            return results

        return [
            res
            for res in results
            if abs(res.duration - self.duration) <= duration_threshold
        ]

    def _filter_track_number(
        self, results: list[deezer.Track]
    ) -> list[deezer.Track]:
        """
        Filter results based on the track number of the track.
        Parameters
        ----------
        results : list[deezer.resources.Track]
            List of Track objects, each of which contains the data of a track.
        Returns
        -------
        list[deezer.resources.Track]
            List of Track objects, each of which contains the data of a track,
            filtered by track number. Only tracks with a track number matching
            the provided one are returned.
        """
        if self.track_number is None or self.strict is False:
            return results

        return [res for res in results if res.track_position == self.track_number]

    def _get_track_by_isrc(self) -> deezer.Track | None:
        """
        Return the Deezer track from a ISRC code.
        Returns
        -------
        deezer.resources.Track
            Deezer isrc of the best match.
        """
        if not self.isrc:
            return None
        for code in self.isrc:
            try:
                return self.deezer_client.request(  # type: ignore
                    method="GET", 
                    path="/track/isrc:" + code, 
                    resource_type=deezer.Track
                )
            except Exception:
                continue

    def best_match(self, duration_threshold: int = 3) -> deezer.Track | None:
        """
        Return the best match for the track.
        If a duration is provided, the best match is the one with the closest
        duration to the provided one. Otherwise, the best match is the first
        result returned by the Deezer API.
        Parameters
        ----------
        duration_threshold : int
            Threshold for the duration difference between the best match and
            the provided duration. If the difference is greater than the
            threshold, an error is raised.
        Returns
        -------
        dict
            Dictionary containing the data of the best match.
        """
        if not self.duration and not self.track_number and not self.isrc:
            result = self._get_data(limit=1)
            return result[0] if result else None

        if self.isrc:
            return self._get_track_by_isrc()

        # if duration or track number exist, get all results
        results = self._get_data()

        if results is None:
            return None

        if len(results) == 1:
            return results[0]
        # filter results by duration
        results = self._filter_duration(results, duration_threshold)
        # filter results by track number
        results = self._filter_track_number(results)

        # if duration is specified, get the closest duration
        if self.duration:
            # get all durations of the filtered results
            durations = [res.duration for res in results]

            # get the closest duration to the provided one
            idx = durations.index(min(durations, key=lambda x: abs(x - self.duration)))  # type: ignore
            return results[idx]

        return results[0] if len(results) > 0 else None

    def get_link(self) -> str | None:
        """
        Return the Deezer link of the best match.
        Returns
        -------
        str
            Deezer link of the best match.
        """
        try:
            return self.best_match().link  # type: ignore
        except AttributeError:
            return None

    def get_duration(self) -> int | None:
        """
        Return the duration of the best match.
        Returns
        -------
        int
            Duration of the best match in seconds.
        """
        try:
            return self.best_match().duration  # type: ignore
        except AttributeError:
            return None

    def get_id(self) -> int | None:
        """
        Return the Deezer ID of the best match.
        Returns
        -------
        int
            Deezer ID of the best match.
        """
        try:
            return self.best_match().id  # type: ignore
        except AttributeError:
            return None

    def get_preview(self) -> str | None:
        """
            Return the Deezer preview of the best match.
            Returns
            -------
            str
                Deezer preview of the best match.
        """
        if self.best_match():
            return self.best_match().preview  # type: ignore

    def get_artist(self) -> deezer.Artist | None:
        """
            Return the Deezer artist of the best match.
            Returns
            -------
            deezer.resources.Artist
                Deezer artist of the best match.
        """
        try:
            return self.best_match().artist  # type: ignore
        except AttributeError:
            return None

    def get_artist_name(self) -> str | None:
        """
            Return the Deezer artist name of the best match.
            Returns
            -------
            str
                Deezer artist name of the best match.
        """
        try:
            return self.get_artist().name  # type: ignore
        except AttributeError:
            return None

    def get_album(self) -> deezer.Album | None:
        """
            Return the Deezer album of the best match.
            Returns
            -------
            deezer.resources.Album
                Deezer album of the best match.
        """
        try:
            return self.best_match().album  # type: ignore
        except AttributeError:
            return None

    def get_album_title(self) -> str | None:
        """
            Return the Deezer album title of the best match.
            Returns
            -------
            str
                Deezer album title of the best match.
        """
        try:
            return self.get_album().title  # type: ignore
        except AttributeError:
            return None

    def get_track(self) -> str | None:
        """
            Return the Deezer track of the best match.
            Returns
            -------
            str
                Deezer track of the best match.
        """
        try:
            return self.best_match().title_short  # type: ignore
        except AttributeError:
            return None

    def get_rank(self) -> int | None:
        """
            Return the Deezer rank of the best match.
            Returns
            -------
            int
                Deezer rank of the best match.
        """
        try:
            return self.best_match().rank  # type: ignore
        except AttributeError:
            return None

    def get_track_number(self) -> int | None:
        """
            Return the Deezer track number of the best match.
            Returns
            -------
            int
                Deezer track number of the best match.
        """
        try:
            return self.best_match().track_position  # type: ignore
        except AttributeError:
            return None

    def get_release_date(self) -> str | None:
        """
            Return the Deezer release date of the best match.
            Returns
            -------
            str
                Deezer release date of the best match.
        """
        try:
            return self.best_match().release_date.strftime("%d/%m/%Y")  # type: ignore
        except AttributeError:
            return None

    def get_bpm(self) -> float | None:
        """
            Return the Deezer bpm of the best match.
            Returns
            -------
            float
                Deezer bpm of the best match.
        """
        try:
            return self.best_match().bpm  # type: ignore
        except AttributeError:
            return None

    def get_isrc(self) -> str | None:
        """
            Return the Deezer isrc of the best match.
            Returns
            -------
            str
                Deezer isrc of the best match.
        """
        try:
            return self.best_match().isrc  # type: ignore
        except AttributeError:
            return None


if __name__ == "__main__":
    # test the DeezerAlign class
    deezer_align = DeezerAlign(
        artist="Louis Armstrong and His Hot Five",
        album=None,
        track="Hotter than that",
        duration=None,
        strict=True,
        track_number=None,
        isrc=["USSM10003868"],
    )
    print(deezer_align.get_track())
    print(deezer_align.get_rank())
    print(deezer_align.get_track_number())
    print(deezer_align.get_release_date())
    print(deezer_align.get_bpm())
