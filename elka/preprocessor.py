"""Script for extracting relevant information from the JAMS files that
will be used for aligning the data with the MusicBrainz database.
"""

import logging
from pathlib import Path

import jams

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JAMSProcess:
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
        self.track_name = self.metadata.title
        self.artist_name = self.metadata.artist
        self.album_name = self.metadata.release
        self.duration = self.metadata.duration

        print(self.track_name)
        print(self.artist_name)
        print(self.album_name)
        print(self.duration)


if __name__ == '__main__':
    # test the class
    jams_file = Path('../partitions/isophonics/choco/jams/isophonics_77.jams')
    output_dir = Path('../partitions/isophonics/choco/jams_aligned/')
    jams_process = JAMSProcess(jams_file, output_dir)

