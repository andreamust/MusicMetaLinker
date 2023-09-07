"""
Scripts for linking tracks to Deezer IDs using the Deezer API and their
search functionalities.
"""

import deezer


class DeezerAlign:
    """
    Search for a track on Deezer and return its data.
    So far, the class supports the following methods:
        - get_data
        - get_link
        - get_duration
        - get_id
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
            track=self.track, artist=self.artist, album=self.album, strict=self.fuzzy,
        )
        if len(results) == 0:
            raise ValueError(f"Track {self.track} not found on Deezer")
        return [res for res in results][:limit]

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
        if self.duration is None and self.track_number is not None:
            return self._get_data(limit=1)[0]
        if self.duration is not None and self.track_number is None:
            return self._get_data(limit=1)[0]

        # if duration exists, get all results
        results = self._get_data()
        durations = [res.duration for res in results]
        idx = durations.index(min(durations, key=lambda x: abs(x - self.duration)))

        # check if the duration of the best match is close enough to the
        # provided duration in strict mode is greater than the threshold,
        # raise an error
        if self.strict and self.duration:
            if abs(results[idx].duration - self.duration) > duration_threshold:
                raise ValueError(
                    "No match found. "
                    f"Closest match: {results[idx].title} by "
                    f"{results[idx].artist.name}"
                )
            valid_results = [
                res
                for res in results
                if abs(res.duration - self.duration) <= duration_threshold
            ]
            if self.strict and self.track_number:
                if results[idx].track_position != self.track_number:
                    raise ValueError(
                        "No match found. "
                        f"Closest match: {results[idx].title} by {results[idx].artist.name}"
                    )

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
        return self.best_match()["duration"]

    def get_id(self) -> int:
        """
        Return the Deezer ID of the best match.
        Returns
        -------
        int
            Deezer ID of the best match.
        """
        return self.best_match()["id"]

    def get_preview(self) -> str:
        """
            Return the Deezer preview of the best match.
            Returns
            -------
            str
                Deezer preview of the best match.
            """
        return self.best_match()["preview"]

    def get_artist(self) -> str:
        """
            Return the Deezer artist of the best match.
            Returns
            -------
            str
                Deezer artist of the best match.
            """
        return self.best_match()["artist"]["name"]

    def get_album(self) -> str:
        """
            Return the Deezer album of the best match.
            Returns
            -------
            str
                Deezer album of the best match.
            """
        return self.best_match()["album"]["title"]

    def get_track(self) -> str:
        """
            Return the Deezer track of the best match.
            Returns
            -------
            str
                Deezer track of the best match.
            """
        return self.best_match()["title"]

    def get_rank(self) -> str:
        """
            Return the Deezer rank of the best match.
            Returns
            -------
            str
                Deezer rank of the best match.
            """
        return self.best_match()["rank"]

    def get_track_number(self) -> str:
        """
            Return the Deezer track number of the best match.
            Returns
            -------
            str
                Deezer track number of the best match.
            """
        return self.best_match()["track_number"]


if __name__ == "__main__":
    # test the DeezerAlign class
    deezer_align = DeezerAlign(
        artist="The Beatles",
        album="With the Beatles",
        track="I Wanna Be Your Man",
        duration=119.973,
        strict=True,
    )
    print(deezer_align.best_match())
    print(deezer_align.get_link())
    print(deezer_align.get_duration())
    print(deezer_align.get_id())
    print(deezer_align.get_preview())
    print(deezer_align.get_artist())
    print(deezer_align.get_album())
    print(deezer_align.get_track())
    print(deezer_align.get_rank())
    # print(deezer_align.get_track_number())
