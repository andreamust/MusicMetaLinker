"""
Scripts for coverting folders to the new format.
"""

import os
import subprocess
from pathlib import Path
import pandas as pd


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


def convert_rwc(output_folder: str | Path) -> None:
    """
    Converts the RWC partition to the new format.
    Returns
    -------
    None
    """
    output_folder = Path(output_folder)
    # get the path to the input folder
    base_path = Path("./partitions/rwc-pop")
    row_audio = base_path / "row" / "audio"
    metadata_path = base_path / "row" / "meta.csv"
    row_metadata = base_path / "row" / "row_meta.txt"
    # get the metadata
    metadata = pd.read_csv(metadata_path)
    row_metadata = pd.read_csv(row_metadata, sep="\t")

    # find correspondences between artist and track names between metadata and
    # row metadata
    for _, row in row_metadata.iterrows():
        # get "Cat. Suffix" and "Tr. No." from the row metadata
        piece_no = row["Piece No."].lstrip("No. ").zfill(3)
        cat_suffix = row["Cat. Suffix"]
        track_no = row["Tr. No."].lstrip("Tr. ")
        print(piece_no, cat_suffix, track_no)
        # get the corresponding row in the metadata, which is in the "file_path"
        # column, format as f'../../partitions/rwc-pop/raw/N{piece_no}-{cat_suffix}-T{track_no}.lab'
        row = metadata[metadata["file_path"] ==
                       f'../../partitions/rwc-pop/raw/N{piece_no}-{cat_suffix}-T{track_no}.lab']
        
        # get the id
        meta_id = row["id"].values[0]
        converted_path = Path(f"{output_folder}/{meta_id}.flac")

        # if output_folder does not exist, create it
        output_folder.mkdir(parents=True, exist_ok=True)

        # original file path
        original_file_path = row_audio / f"RM-P{piece_no}.wav"
        print(original_file_path, original_file_path.exists())
        if original_file_path.exists():
            # convert the file to FLAC
            subprocess.call(['ffmpeg', '-i', original_file_path,
                            '-c:a', 'flac', converted_path,])
        else:
            raise FileNotFoundError(f"{original_file_path} does not exist")


if __name__ == '__main__':
    # convert the Schubert Winterreise partition
    # convert_schubert()

    # convert the RWC partition
    convert_rwc('./partitions/rwc-pop/choco/audio')
