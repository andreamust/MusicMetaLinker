"""
Scripts for linking tracks to Deezer IDs using the Deezer API and their
search functionalities.
"""

import deezer


class DeezerAlign:
    """
    Search for a track on Deezer and return its data.
    """

    def __init__(
        self,
        artist: str = None,
        album: str = None,
        track: str = None,
        track_number: int = None,
        duration: float = None,
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
        if artist is None and album is None and track is None:
            raise ValueError(
                "No parameters passed. "
                "Please specify at least one parameter among the "
                "following: artist, album, track."
            )

        self.artist = artist
        self.album = album
        self.track = track
        self.track_number = track_number
        self.duration = duration
        self.strict = strict
        self.fuzzy = False if fuzzy is True else True

        # connect to Deezer API
        self.deezer_client = deezer.Client()

    def _get_data(self, limit: int = None) -> list[deezer.resources.Track]:
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
            track=self.track,
            artist=self.artist,
            album=self.album,
            strict=self.fuzzy,
        )

        if len(results) == 0:
            raise ValueError(f"Track {self.track} not found on Deezer")
        return [res for res in results][:limit]

    def _filter_duration(
        self, results: list[deezer.resources.Track], duration_threshold: int
    ) -> list[deezer.resources.Track]:
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
        self, results: list[deezer.resources.Track]
    ) -> list[deezer.resources.Track]:
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

    def best_match(self, duration_threshold: int = 3) -> deezer.resources.Track:
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
        if self.duration is None and self.track_number is None:
            return self._get_data(limit=1)[0]

        # if duration or track number exist, get all results
        results = self._get_data()
        # filter results by duration
        results = self._filter_duration(results, duration_threshold)
        # filter results by track number
        results = self._filter_track_number(results)

        # get all durations of the filtered results
        durations = [res.duration for res in results]

        # get the closest duration to the provided one
        idx = durations.index(min(durations, key=lambda x: abs(x - self.duration)))

        return results[idx]

    def get_link(self) -> str:
        """
        Return the Deezer link of the best match.
        Returns
        -------
        str
            Deezer link of the best match.
        """
        return self.best_match().link

    def get_duration(self) -> int:
        """
        Return the duration of the best match.
        Returns
        -------
        int
            Duration of the best match in seconds.
        """
        return self.best_match().duration

    def get_id(self) -> int:
        """
        Return the Deezer ID of the best match.
        Returns
        -------
        int
            Deezer ID of the best match.
        """
        return self.best_match().id

    def get_preview(self) -> str:
        """
            Return the Deezer preview of the best match.
            Returns
            -------
            str
                Deezer preview of the best match.
        """
        return self.best_match().preview

    def get_artist(self) -> deezer.resources.Artist:
        """
            Return the Deezer artist of the best match.
            Returns
            -------
            deezer.resources.Artist
                Deezer artist of the best match.
        """
        return self.best_match().artist

    def get_artist_name(self) -> str:
        """
            Return the Deezer artist name of the best match.
            Returns
            -------
            str
                Deezer artist name of the best match.
        """
        return self.get_artist().name

    def get_album(self) -> deezer.resources.Album:
        """
            Return the Deezer album of the best match.
            Returns
            -------
            deezer.resources.Album
                Deezer album of the best match.
        """
        return self.best_match().album

    def get_album_title(self) -> str:
        """
            Return the Deezer album title of the best match.
            Returns
            -------
            str
                Deezer album title of the best match.
        """
        return self.get_album().title

    def get_track(self) -> str:
        """
            Return the Deezer track of the best match.
            Returns
            -------
            str
                Deezer track of the best match.
        """
        return self.best_match().title_short

    def get_rank(self) -> int:
        """
            Return the Deezer rank of the best match.
            Returns
            -------
            int
                Deezer rank of the best match.
        """
        return self.best_match().rank

    def get_track_number(self) -> int:
        """
            Return the Deezer track number of the best match.
            Returns
            -------
            int
                Deezer track number of the best match.
        """
        return self.best_match().track_position

    def get_release_date(self) -> str:
        """
            Return the Deezer release date of the best match.
            Returns
            -------
            str
                Deezer release date of the best match.
        """
        return self.best_match().release_date.strftime("%d/%m/%Y")

    def get_bpm(self) -> float:
        """
            Return the Deezer bpm of the best match.
            Returns
            -------
            float
                Deezer bpm of the best match.
        """
        return self.best_match().bpm


if __name__ == "__main__":
    # test the DeezerAlign class
    deezer_align = DeezerAlign(
        artist="",
        album="",
        track="I Wanna Be Your Man",
        duration=118.973,
        strict=True,
        track_number=11,
    )
    print(deezer_align.best_match())
    print(deezer_align.get_link())
    print(deezer_align.get_duration())
    print(deezer_align.get_id())
    print(deezer_align.get_preview())
    print(deezer_align.get_artist())
    print(deezer_align.get_artist_name())
    print(deezer_align.get_album())
    print(deezer_align.get_album_title())
    print(deezer_align.get_track())
    print(deezer_align.get_rank())
    print(deezer_align.get_track_number())
    print(deezer_align.get_release_date())
    print(deezer_align.get_bpm())
