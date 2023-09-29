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

from acousticbrainz_links import acousticbrainz_link
from deezer_links import DeezerAlign
from musicbrainz_links import MusicBrainzAlign
from youtube_links import YouTubeAlign


class Align:
    """
    A class that aligns metadata of a track and parameters for search.

    Attributes
    ----------
    mbid_track : str
        MusicBrainz ID of the track.
    mbid_release : str
        MusicBrainz ID of the release.
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

    Methods
    -------
    get_artist() -> str:
        Returns the artist name.
    get_album() -> str:
        Returns the album name.
    get_track() -> str:
        Returns the track name.
    get_track_number() -> int | None:
        Returns the track number.
    get_duration() -> float:
        Returns the track duration.
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
        isrc: str | list | None = None,
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
        self.mbid_track = mbid_track
        self.mbid_release = mbid_release
        self.artist = artist
        self.album = album
        self.track = track
        self.track_number = track_number
        self.duration = duration
        self.isrc = isrc
        self.strict = strict

        if isinstance(self.isrc, str):
            self.isrc = [self.isrc]

        # check that the MusicBrainz ID is valid
        if self.mbid_track:
            try:
                self.isrc = self.mb_link.get_isrc()
                self.track = self.mb_link.get_track() if not self.track else self.track
                self.artist = (
                    self.mb_link.get_artist() if not self.artist else self.artist
                )
            except musicbrainzngs.musicbrainz.ResponseError:
                self.mbid_track = None

    @property
    def mb_link(self):
        """
        Initializes the MusicBrainz link.
        """
        return MusicBrainzAlign(
            mbid_track=self.mbid_track,
            mbid_release=self.mbid_release,
            artist=self.artist,
            album=self.album,
            track=self.track,
            track_number=self.track_number,
            duration=self.duration,
            isrc=self.isrc,
            strict=self.strict,
        )
    
    @property
    def dz_link(self):
        """
        Initializes the Deezer link.
        """
        return DeezerAlign(
            artist=self.artist,
            album=self.album,
            track=self.track,
            track_number=self.track_number,
            duration=self.duration,
            isrc=self.isrc,
            strict=self.strict,
        )

    @property
    def yt_link(self):
        """
        Initializes the YouTube link.
        """
        return YouTubeAlign(
            artist=self.artist,
            album=self.album,
            track=self.track,
            track_number=self.track_number,
            duration=self.duration,
            isrc=self.isrc,
            strict=self.strict,
        )

    def get_artist(self) -> str | None:
        """
        Returns the artist name.

        Returns
        -------
        str
            Artist name.
        """
        artist = None

        if self.artist:
            return self.artist
        elif self.mbid_track:
            artist = self.mb_link.get_artist()

        # check iteratively on all the implemented platforms
        if artist is None:
            artist = self.dz_link.get_artist_name()
            if artist is None:
                artist = self.mb_link.get_artist()
                if artist is None:
                    artist = self.yt_link.get_youtube_artist()
        return artist

    def get_album(self) -> str | None:
        """
        Returns the album name.

        Returns
        -------
        str
            Album name.
        """
        album = None

        if self.album:
            return self.album
        elif self.mbid_track:
            album = self.mb_link.get_album()

        # check iteratively on all the implemented platforms
        if album is None:
            album = self.dz_link.get_album_title()
            if album is None:
                album = self.mb_link.get_album()
                if album is None:
                    album = self.yt_link.get_youtube_album()
        return album

    def get_track(self) -> str | None:
        """
        Returns the track name.

        Returns
        -------
        str
            Track name.
        """
        track = None

        if self.track:
            return self.track
        elif self.mbid_track:
            track = self.mb_link.get_track()

        # check iteratively on all the implemented platforms
        if track is None:
            track = self.dz_link.get_track()
            if track is None:
                track = self.mb_link.get_track()
                if track is None:
                    track = self.yt_link.get_youtube_title()
        return track

    def get_track_number(self) -> int | None:
        """
        Returns the track number.

        Returns
        -------
        int
            Track number.
        """
        track_number = None

        if self.track_number:
            return self.track_number
        elif self.mbid_track:
            track_number = self.mb_link.get_track_number()

        # check iteratively on all the implemented platforms
        if track_number is None:
            track_number = self.dz_link.get_track_number()
            if track_number is None:
                track_number = self.mb_link.get_track_number()
        return track_number

    def get_duration(self) -> float | None:
        """
        Returns the track duration.

        Returns
        -------
        float
            Track duration.
        """
        duration = None

        if self.duration:
            return self.duration
        elif self.mbid_track:
            duration = self.mb_link.get_duration()

        # check iteratively on all the implemented platforms
        if duration is None:
            duration = self.dz_link.get_duration()
            if duration is None:
                duration = self.mb_link.get_duration()
                if duration is None:
                    duration = self.yt_link.get_youtube_duration()
        return duration

    def get_isrc(self) -> str | list[str] | None:
        """
        Returns the ISRC code.
        Returns
        -------
        list[str]
            ISRC codes.
        """
        isrc = None

        if self.isrc:
            return self.isrc
        elif self.mbid_track:
            isrc = self.mb_link.get_isrc()

        # check on deezer
        if isrc is None:
            isrc = self.dz_link.get_isrc()
            if isrc is None:
                isrc = self.mb_link.get_isrc()

        self.isrc = isrc
        return isrc

    def get_release_date(self) -> str | None:
        """
        Returns the release date.
        Returns
        -------
        str
            Release date.
        """
        if self.mbid_track:
            return self.mb_link.get_release_date()
        return self.dz_link.get_release_date()

    def get_mbid(self) -> str | None:
        """
        Returns the MusicBrainz ID.
        Returns
        -------
        str
            MusicBrainz ID.
        """
        if self.mbid_track:
            return self.mbid_track
        return self.mb_link.get_mbid()

    def get_deezer_id(self) -> int | None:
        """
        Returns the Deezer ID.
        Returns
        -------
        int
            Deezer ID.
        """
        return self.dz_link.get_id()

    def get_deezer_link(self) -> str | None:
        """
        Returns the Deezer link.
        Returns
        -------
        str
            Deezer link.
        """
        return self.dz_link.get_link()

    def get_youtube_link(self) -> str | None:
        """
        Returns the YouTube link.
        Returns
        -------
        str
            YouTube link.
        """
        return self.yt_link.get_youtube_link()

    def get_bpm(self) -> float | None:
        """
        Returns the BPM.
        Returns
        -------
        float
            BPM.
        """
        return self.dz_link.get_bpm()

    def get_acousticbrainz_link(self) -> str | None:
        """
        Returns the AcousticBrainz link.
        Returns
        -------
        str
            AcousticBrainz link.
        """
        if self.mbid_track:
            return acousticbrainz_link(self.mbid_track)


if __name__ == "__main__":
    # test the class
    aligner = Align(
        artist="The Beatles",
        album="The Beatles CD1",
        track="Black Bird",
        track_number=None,
        duration=None,
        isrc=None,
        strict=False,
    )
    print("Artist:", aligner.get_artist())
    print("Album:", aligner.get_album())
    print("Track:", aligner.get_track())
    print("Track number:", aligner.get_track_number())
    print("Duration:", aligner.get_duration())
    print("ISRC:", aligner.get_isrc())
    print("Release date:", aligner.get_release_date())
    print("MusicBrainz ID:", aligner.get_mbid())
    print("Deezer ID:", aligner.get_deezer_id())
    print("Deezer link:", aligner.get_deezer_link())
    print("YouTube link:", aligner.get_youtube_link())
    print("BPM:", aligner.get_bpm())
    print("AcousticBrainz link:", aligner.get_acousticbrainz_link())
