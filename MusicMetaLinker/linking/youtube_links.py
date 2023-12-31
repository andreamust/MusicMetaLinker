"""
Searches for musicbrainz id on ListerBrainz for retrieving the YouTube links.
"""

from ytmusicapi import YTMusic


class YouTubeAlign:
    """
    Class for retrieving the YouTube links given the track metadata.
    """

    def __init__(
        self,
        track: str | None = None,
        artist: str | None = None,
        album: str | None = None,
        track_number: int | None = None,
        duration: float | None = None,
        isrc: list | str | None = None,
        strict: bool = False,
    ) -> None:
        """
        Initializes the class by taking the metadata of the track and the
        parameters for the search.
        Parameters
        ----------
        track : str
            Track name.
        artist : str
            Artist name.
        album : str
            Album name.
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
        self.track = track
        self.artist = artist
        self.album = album
        self.track_number = track_number
        self.duration = duration
        self.isrc = isrc
        self.strict = strict

        print(f"Searching for {self.artist} - {self.track} on YouTube Music")

        self.yt = YTMusic()

    def _search(self) -> list:
        """
        Searches for the track on YouTube Music.
        Returns
        -------
        list
            List of results.
        """
        # search for the track
        results = self.yt.search(
            f"{self.artist} {self.track} {self.album}",
            filter="songs",
            ignore_spelling=self.strict,
        )
        return results

    def _filter_duration(self, results: list, duration_threshold: int) -> list:
        """
        Filters the results by keeping only tracks that have a duration
        difference less than the threshold.
        Parameters
        ----------
        results : list
            List of results.
        duration_threshold : int
            Duration threshold in seconds.
        Returns
        -------
        list
            List of filtered results.
        """
        if not self.duration:
            return results
        filtered_results = []
        for result in results:
            if abs(result["duration_seconds"] - self.duration) <= duration_threshold:
                filtered_results.append(result)
        return filtered_results

    def get_best_match(self) -> dict | None:
        """
        Returns the best match for the track.
        Returns
        -------
        dict
            Dictionary containing the best match.
        """
        # search for the track
        results = self._search()
        # filter the results
        # results = self._filter_duration(results, 10)
        # return the best match
        if results:
            return results[0]
        return None

    def get_youtube_link(self) -> str | None:
        """
        Returns the YouTube link for the best match.
        Returns
        -------
        str
            YouTube link.
        """
        best_match = self.get_best_match()
        try:
            return f"https://music.youtube.com/watch?v={best_match['videoId']}"  # type: ignore
        except (KeyError, TypeError):
            return None

    def get_youtube_id(self) -> str | None:
        """
        Returns the YouTube ID for the best match.
        Returns
        -------
        str
            YouTube link.
        """
        best_match = self.get_best_match()
        try:
            return f"{best_match['videoId']}"  # type: ignore
        except (KeyError, TypeError):
            return None

    def get_youtube_title(self) -> str | None:
        """
        Returns the YouTube title for the best match.
        Returns
        -------
        str
            YouTube link.
        """
        best_match = self.get_best_match()
        try:
            return f"{best_match['title']}"  # type: ignore
        except (KeyError, TypeError):
            return None

    def get_youtube_artist(self) -> str | None:
        """
        Returns the YouTube artist name for the best match.
        Returns
        -------
        str
            YouTube link.
        """
        best_match = self.get_best_match()
        try:
            return f"{best_match['artists'][0]['name']}"  # type: ignore
        except (KeyError, TypeError):
            return None

    def get_youtube_album(self) -> str | None:
        """
        Returns the YouTube album name for the best match.
        Returns
        -------
        str
            YouTube link.
        """
        best_match = self.get_best_match()
        try:
            return f"{best_match['album']['name']}"  # type: ignore
        except (KeyError, TypeError):
            return None

    def get_youtube_duration(self) -> int | None:
        """
        Returns the YouTube duration in seconds for the best match.
        Returns
        -------
        str
            YouTube link.
        """
        best_match = self.get_best_match()
        try:
            return best_match["duration_seconds"]  # type: ignore
        except (KeyError, TypeError):
            return None

    def get_youtube_release_date(self) -> str | None:
        """
        Returns the YouTube release date for the best match.
        Returns
        -------
        str
            YouTube link.
        """
        best_match = self.get_best_match()
        try:
            return f"{best_match['year']}"  # type: ignore
        except (KeyError, TypeError):
            return None


if __name__ == "__main__":
    # test the class
    yt = YouTubeAlign(
        track="Baby Won't You Please Come Home",
        artist="Henry Allen",
        album="The Cradle Of Jazz",
        duration=89,
    )
    print(yt.get_youtube_link())
    print(yt.get_youtube_id())
    print(yt.get_youtube_title())
    print(yt.get_youtube_artist())
    print(yt.get_youtube_album())
    print(yt.get_youtube_duration())
    print(yt.get_youtube_release_date())
