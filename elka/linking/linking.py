"""
Scripts for retrieving links of the audio partitions form the following
repositories:
    - MusicBrainz
    - Deezer
    - YouTube Music
    - AcousticBrainz

The scripts are based on the following libraries:
    - musicbrainzngs
    - deezer-python
    - youtube-search-python

The library will be expanded in the future to support more repositories, such
as Spotify, YouTube, etc.
"""
import musicbrainzngs.musicbrainz

from .acousticbrainz_links import acousticbrainz_link
from .deezer_links import DeezerAlign
from .musicbrainz_links import MusicBrainzAlign
from .youtube_links import YouTubeAlign


class Align:
    """
    Class for creating links between the audio partitions and the external
    resources.
    So far, the following repositories are supported:
        - MusicBrainz
        - Deezer
        - YouTube Music
    """

    def __init__(
        self,
        mbid: str = None,
        artist: str = None,
        album: str = None,
        track: str = None,
        track_number: int = None,
        duration: float = None,
        isrc: str | list = None,
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
        isrc : str | list
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

        if isinstance(self.isrc, str):
            self.isrc = [self.isrc]

        self.mb_link = MusicBrainzAlign(
            mbid=self.mbid,
            artist=self.artist,
            album=self.album,
            track=self.track,
            track_number=self.track_number,
            duration=self.duration,
            isrc=self.isrc,
            strict=self.strict,
        )

        # check that the MusicBrainz ID is valid
        if self.mbid:
            try:
                self.isrc = self.mb_link.get_isrc()
                self.track = self.mb_link.get_track() if not self.track else self.track
                self.artist = (
                    self.mb_link.get_artist() if not self.artist else self.artist
                )
            except musicbrainzngs.musicbrainz.ResponseError:
                self.mbid = None

        self.dz_link = DeezerAlign(
            artist=self.artist,
            album=self.album,
            track=self.track,
            track_number=self.track_number,
            duration=self.duration,
            isrc=self.isrc,
            strict=False,
        )

        self.yt_link = YouTubeAlign(
            artist=self.artist,
            album=self.album,
            track=self.track,
            track_number=self.track_number,
            duration=self.duration,
            isrc=self.isrc,
            strict=False,
        )

    def get_artist(self) -> str:
        """
        Returns the artist name.
        Returns
        -------
        str
            Artist name.
        """
        if self.artist:
            return self.artist
        elif self.mbid:
            return self.mb_link.get_artist()
        else:
            try:
                return self.yt_link.get_youtube_artist()
            except ValueError:
                return self.dz_link.get_artist()

    def get_album(self) -> str:
        """
        Returns the album name.
        Returns
        -------
        str
            Album name.
        """
        if self.album:
            return self.album
        elif self.mbid:
            return self.mb_link.get_album()
        else:
            try:
                return self.yt_link.get_youtube_album()
            except ValueError:
                return self.dz_link.get_album()

    def get_track(self) -> str:
        """
        Returns the track name.
        Returns
        -------
        str
            Track name.
        """
        if self.track:
            return self.track
        elif self.mbid:
            return self.mb_link.get_track()
        else:
            try:
                return self.yt_link.get_youtube_title()
            except ValueError:
                return self.dz_link.get_track()

    def get_track_number(self) -> int | None:
        """
        Returns the track number.
        Returns
        -------
        int
            Track number.
        """
        if self.track_number:
            return self.track_number
        try:
            return self.dz_link.get_track_number()
        except ValueError:
            return None

    def get_duration(self) -> float:
        """
        Returns the track duration.
        Returns
        -------
        float
            Track duration.
        """
        if self.duration:
            return self.duration
        elif self.mbid:
            try:
                return self.mb_link.get_duration()
            except Exception:
                pass
        else:
            try:
                return self.yt_link.get_youtube_duration()
            except ValueError:
                return self.dz_link.get_duration()

    def get_isrc(self) -> list[str] | None:
        """
        Returns the ISRC code.
        Returns
        -------
        list[str]
            ISRC codes.
        """
        if self.isrc:
            return self.isrc
        elif self.mbid:
            try:
                return self.mb_link.get_isrc()
            except Exception:
                return None
        else:
            try:
                return [self.dz_link.get_isrc()]
            except ValueError:
                return None

    def get_release_date(self) -> str:
        """
        Returns the release date.
        Returns
        -------
        str
            Release date.
        """
        if self.mbid:
            return self.mb_link.get_release_date()
        try:
            return self.dz_link.get_release_date()
        except ValueError:
            return None

    def get_mbid(self) -> str | None:
        """
        Returns the MusicBrainz ID.
        Returns
        -------
        str
            MusicBrainz ID.
        """
        if self.mbid:
            return self.mbid
        try:
            return self.mb_link.get_mbid()
        except Exception:
            return None

    def get_deezer_id(self) -> int | None:
        """
        Returns the Deezer ID.
        Returns
        -------
        int
            Deezer ID.
        """
        try:
            return self.dz_link.get_id()
        except ValueError:
            return None

    def get_deezer_link(self) -> str | None:
        """
        Returns the Deezer link.
        Returns
        -------
        str
            Deezer link.
        """
        try:
            return self.dz_link.get_link()
        except ValueError:
            return None

    def get_youtube_link(self) -> str | None:
        """
        Returns the YouTube link.
        Returns
        -------
        str
            YouTube link.
        """
        try:
            return self.yt_link.get_youtube_link()
        except ValueError:
            return None

    def get_bpm(self) -> float | None:
        """
        Returns the BPM.
        Returns
        -------
        float
            BPM.
        """
        try:
            return self.dz_link.get_bpm()
        except ValueError:
            return None

    def get_acousticbrainz_link(self) -> str | None:
        """
        Returns the AcousticBrainz link.
        Returns
        -------
        str
            AcousticBrainz link.
        """
        if self.mbid:
            return acousticbrainz_link(self.mbid)
        return None


if __name__ == "__main__":
    # test the class
    aligner = Align(
        mbid="5478f78d-3cbc-4940-ab18-c605dd67b236",
        artist="Louis Armstrong",
        album=None,
        track=None,
        track_number=None,
        duration=None,
        isrc=None,
        strict=True,
    )
    print(aligner.get_artist())
    print(aligner.get_album())
    print(aligner.get_track())
    print(aligner.get_track_number())
    print(aligner.get_duration())
    print(aligner.get_isrc())
    print(aligner.get_release_date())
    print(aligner.get_mbid())
    print(aligner.get_deezer_id())
    print(aligner.get_deezer_link())
    print(aligner.get_youtube_link())
