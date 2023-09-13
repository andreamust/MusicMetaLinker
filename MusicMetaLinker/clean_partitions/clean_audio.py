"""
Scripts for cleaning the JAAH partition.
"""

from pathlib import Path

import pandas as pd


def clean_audio(audio_files: Path, metadata_file: Path) -> None:
    """
    Cleans the JAAH partition.
    Parameters
    ----------
    audio_files : Path
        Path to the audio files.
    metadata_file : Path
        Path to the metadata file.
    Returns
    -------
    None
    """
    # read the metadata
    metadata = pd.read_csv(metadata_file)
    valid_extensions = [".mp3", ".wav", ".m4a", ".flac", ".ogg", ".mp4", ".wma"]
    # iterate over the audio files
    for audio_file in audio_files.iterdir():
        if audio_file.suffix not in valid_extensions:
            continue
        print(f"Processing audio file {audio_file.name}")
        # get the audio file name
        audio_file_name = audio_file.stem
        # get the metadata
        try:
            file_title = metadata.loc[
                metadata["file_title"] == audio_file_name, "id"
            ].values[0]
            # log the renaming data
            print(f"Renaming {audio_file_name} to {file_title}")
            # rename the file
            audio_file.rename(audio_file.parent / f"{file_title}{audio_file.suffix}")
        except IndexError:
            continue


if __name__ == "__main__":
    # clean the JAAH partition
    clean_audio(
        Path("../../partitions/jaah/choco/audio"),
        Path("../../partitions/jaah/choco/meta.csv"),
    )

    # clean the schubert-winterreise partition
    clean_audio(
        Path("../../partitions/schubert-winterreise/choco/audio"),
        Path("../../partitions/schubert-winterreise/choco/meta.csv"),
    )
