"""Script for extracting relevant information from the JAMS files that
will be used for aligning the data with the MusicBrainz database.
"""

import logging
from pathlib import Path

import namespaces
import jams

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JAMSProcessor:
    """
    Class for extracting relevant information from the JAMS files that will be
    used for aligning the data with the external resources, as well as for
    writing them in a new JAMS file.
    """

    def __init__(self, jams_file: Path) -> None:
        """
        Initializes the class by taking the path to the JAMS file and the output
        directory where the extracted information will be saved.
        Parameters
        ----------
        jams_file : Path
            Path to the JAMS file.
        Returns
        -------
        None
        """
        self.jams_file = jams_file
        # Load the JAMS file
        self.jams = jams.JAMS.loads(jams_file.read_text())
        # Create a new JAMS file
        self.jams_new = jams.JAMS()

        # get the metadata
        self.metadata = self.jams.file_metadata
        # get the sandbox
        self.sandbox = self.jams.sandbox

        # get individual metadata
        self.track_name = self.metadata.title
        self.artist_name = self.metadata.artist
        if isinstance(self.artist_name, list):
            self.artist_name = self.artist_name[0]
        self.album_name = self.metadata.release
        self.duration = self.metadata.duration
        self.identifiers = self.metadata.identifiers
        self.jams_version = self.metadata.jams_version
        self.musicbrainz_id = None
        if 'musicbrainz' in self.metadata.identifiers.keys():
            self.musicbrainz_id = self.metadata.identifiers['musicbrainz']

        # get individual sandbox
        try:
            self.type = self.sandbox['type']
        except KeyError:
            self.type = 'score'
        self.genre = self.sandbox['genre']
        try:
            self.track_number = self.sandbox.track_number  # type: ignore
            self.release_year = self.sandbox.release_year  # type: ignore
            self.composers = self.sandbox.composers  # type: ignore
            self.performers = self.sandbox.performers  # type: ignore
        except AttributeError:
            self.track_number = None
            self.release_year = None
            self.composers = None
            self.performers = None
        self.tuning = None
        if 'tuning' in self.sandbox.keys():
            self.tuning = self.sandbox.tuning  # type: ignore
        if not self.artist_name and (self.composers or self.performers):
            if self.type == 'score':
                self.artist_name = 'and'.join(self.composers)  # type: ignore
            elif self.type == 'audio':
                self.artist_name = 'and'.join(self.performers)  # type: ignore

    def write_jams(self, output_path: Path) -> None:
        """
        Writes the extracted information in a new JAMS file.
        """
        if not output_path.exists():
            output_path.mkdir(parents=True)
        new_metadata = jams.FileMetadata(
            title=self.track_name,
            artist=self.artist_name,
            release=self.album_name,
            duration=self.duration,
            identifiers=self.identifiers,
            jams_version=self.jams_version,
        )

        new_sandbox = jams.Sandbox(
            type=self.type,
            genre=self.genre,
            track_number=self.track_number,
            release_year=self.release_year,
            composers=self.composers,
            performers=self.performers,
            tuning=self.tuning,
        )

        # add the metadata
        self.jams_new.file_metadata = new_metadata
        # add the sandbox
        self.jams_new.sandbox = new_sandbox
        # add the annotations
        self.jams_new.annotations.append(self.jams.annotations[0])
        # write the JAMS file
        self.jams_new.save(str(output_path / self.jams_file.name),
                           strict=False)


if __name__ == '__main__':
    # test the class
    jams_file = Path('../partitions/isophonics/choco/jams/isophonics_77.jams')
    # output_dir = Path('../partitions/isophonics/choco/jams_aligned/')
    jams_process = JAMSProcessor(jams_file)
    print(jams_process.track_name)
