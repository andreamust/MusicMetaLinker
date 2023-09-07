"""
Scripts for retrieving links of the audio partitions form the following
repositories:
    - MusicBrainz
    - Deezer

The scripts are based on the following libraries:
    - musicbrainzngs
    - deezer-python

The library will be expanded in the future to support more repositories, such
as Spotify, YouTube, etc.
"""

from musicbrainzngs import musicbrainz as mbz
import deezer
import musicbrainzngs as mbz

# The Beatles CD1 / CD2 == The Beatles (the white album)


class FindLink:
    """
    Search for a track external link.
    So far, the class supports the following repositories:
        - Deezer
        - MusicBrainz
    """

    def __init__(self, artist: str, album: str, track: str):
        """
        Parameters
        ----------
        artist : str
            Artist name.
        album : str
            Album name.
        track : str
            Track name.
        """
        self.artist = artist
        self.album = album
        self.track = track

    def search_deezer(self) -> str:
        """
        Search for a track on Deezer.
        Returns
        -------
        str
            Deezer URL of the track.
        Raises
        ------
        ValueError
            If the track is not found.
        """
        deezer_client = deezer.Client()
        results = deezer_client.search(track=self.track,
                                    artist=self.artist,
                                    album=self.album,
                                    strict=False)
        if len(results) == 0:
            raise ValueError(f"Track {self.track} not found on Deezer")
        return results[0].link

    def deezer_duration(self) -> int:
        """
        Search for the duration of the track on Deezer.
        Returns
        -------
        int
            Duration of the track in seconds.
        """
        deezer_client = deezer.Client()
        results = deezer_client.search(track=self.track,
                                    artist=self.artist,
                                    album=self.album,
                                    strict=False)
        if len(results) == 0:
            raise ValueError(f"Track {self.track} not found on Deezer")
        return results[0].duration

    def search_musicbrainz(self) -> str:
        """
        Search for a track on MusicBrainz.
        Returns
        -------
        str
            MusicBrainz URL of the track.
        Raises
        ------
        ValueError
            If the track is not found.
        """
        mbz.set_useragent("elka", "0.1", "http://test.elka.com")
        results = mbz.search_recordings(query=f"artist:{self.artist} "
                                            f"AND release:{self.album} "
                                            f"AND recording:{self.track}")
        if len(results["recording-list"]) == 0:
            raise ValueError(f"Track {self.track} not found on MusicBrainz")
        return results["recording-list"][0]["id"]

if __name__ == '__main__':
    # Test the class
    artist = ""
    album = "The Beatles"
    track = "I Wanna Be Your Man"
    fl = FindLink(artist, album, track)
    print(fl.search_deezer())
    print(fl.deezer_duration())
    print(fl.search_musicbrainz())
    
