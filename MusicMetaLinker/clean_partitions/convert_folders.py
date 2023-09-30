"""
Scripts for coverting folders to the new format.
"""

import os
import subprocess
from pathlib import Path


def convert_folder_to_flac(input_folder: Path, output_folder: Path) -> None:
    """
    Converts all the audio files contained in the input folder to FLAC format.
    Parameters
    ----------
    input_folder : Path
        Path to the input folder.
    output_folder : Path
        Path to the output folder.

    Returns
    -------
    None
    """
    # create the output folder if it does not exist
    output_folder.mkdir(parents=True, exist_ok=True)
    # iterate over the files in the input folder
    for file in input_folder.iterdir():
        # check if the file is an audio file
        if file.suffix in [".wav", ".mp3", ".aiff", ".m4a", ".ogg", ".mp4"]:
            # create the output file path
            output_file = output_folder / (file.stem + ".flac")
            # convert the file to FLAC
            subprocess.call(['ffmpeg', '-i', file,
                             '-c:a', 'flac', output_file,])


def convert_schubert() -> None:
    """
    Converts the Schubert Winterreise partition to the new format.
    Returns
    -------
    None
    """
    # get the path to the input folder
    print(os.getcwd())
    input_folder = Path("./partitions/schubert-winterreise/row")
    # get the path to the output folder
    output_folder = Path("./partitions/schubert-winterreise/choco/audio")
    print(output_folder)
    # convert the folder to FLAC
    convert_folder_to_flac(input_folder, output_folder)


def convert_rwc() -> None:
    """
    Converts the RWC partition to the new format.
    Returns
    -------
    None
    """
    # get the path to the input folder
    input_folder = Path("./partitions/rwc-pop/row/audio")
    # get the path to the output folder
    output_folder = Path("./partitions/rwc-pop/choco/audio")
    # convert the folder to FLAC
    convert_folder_to_flac(input_folder, output_folder)


if __name__ == '__main__':
    # convert the Schubert Winterreise partition
    # convert_schubert()

    # convert the RWC partition
    convert_rwc()
