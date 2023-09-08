"""Script for extracting relevant information from the JAMS files that
will be used for aligning the data with the MusicBrainz database.
"""

import logging
from pathlib import Path

import jams

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JAMSProcessor:
    """
    Class for extracting relevant information from the JAMS files that will be
    used for aligning the data with the external resources, as well as for
    writing them in a new JAMS file.
    """
    def __init__(self, jams_file: Path, output_dir: Path) -> None:
        """
        Initializes the class by taking the path to the JAMS file and the output
        directory where the extracted information will be saved.
        Parameters
        ----------
        jams_file : Path
            Path to the JAMS file.
        output_dir : Path
            Path to the output directory.
        Returns
        -------
        None
        """
        self.jams_file = jams_file
        self.output_dir = output_dir
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)
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
        self.album_name = self.metadata.release
        self.duration = self.metadata.duration
        self.identifiers = self.metadata.identifiers
        self.musicbrainz_id = None
        if 'musicbrainz' in self.metadata.identifiers.keys():
            self.musicbrainz_id = self.metadata.identifiers['musicbrainz']

        # get individual sandbox
        self.type = self.sandbox['type']
        self.track_number = self.sandbox.track_number
        self.release_year = self.sandbox.release_year
        self.composers = 'and'.join(self.sandbox.composers)
        self.performers = 'and'.join(self.sandbox.performers)
        if not self.artist_name:
            if self.type == 'score':
                self.artist_name = self.composers
            elif self.type == 'audio':
                self.artist_name = self.performers

    def write_jams(self) -> None:
        """
        Writes the extracted information in a new JAMS file.
        """
        # add the metadata
        self.jams_new.file_metadata = self.metadata
        # add the sandbox
        self.jams_new.sandbox = self.sandbox
        # add the annotations
        self.jams_new.annotations.append(self.jams.annotations[0])
        # write the JAMS file
        self.jams_new.save(self.output_dir / self.jams_file.name)


if __name__ == '__main__':
    # test the class
    jams_file = Path('../partitions/isophonics/choco/jams/isophonics_77.jams')
    output_dir = Path('../partitions/isophonics/choco/jams_aligned/')
    jams_process = JAMSProcessor(jams_file, output_dir)
    print(jams_process.track_name)

