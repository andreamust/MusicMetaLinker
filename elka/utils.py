"""
Utility functions for the elka package.
"""
from pathlib import Path

import pandas as pd

from partitions_map import AUDIO_PARTITIONS


def log_downloaded_data(data: pd.DataFrame,
                        output_file: Path,
                        output_format: str = "csv") -> None:
    """
    Logs the downloaded data to a file.

    Parameters
    ----------
    data : pd.DataFrame
        Data to be logged.
    output_path : str
        Path to the output directory.
    output_file : str
        Name of the output file.
    output_format : str
        Format of the output file.

    Returns
    -------
    None
    """
    if output_format == "csv":
        data.to_csv(output_file, index=False)
    elif output_format == "json":
        data.to_json(output_file, orient="records", indent=4)
    else:
        raise ValueError("Unsupported output format.")

def reformat_filenames(partitions_path: Path) -> None:
    """
    Iterate over all the audio files in all the AUDIO partitions and rename
    files by removing the .jams string within the filename.
    Parameters
    ----------
    partitions_path : Path
        Path to the partitions.
    Returns
    -------
    None
    """
    for partition in partitions_path.iterdir():
        if partition.name not in AUDIO_PARTITIONS:
            continue
        print(f"Processing partition {partition.name}")
        # partition/choco/jams_converted if exists else partition/choco/jams
        jams_path = partition / "choco" / "audio"

        if partition.name == "schubert-winterreise":
            jams_path = partition / "choco" / "audio" / "audio"
        # iterate over the JAMS files
        for audio_file in jams_path.glob("*.mp3"):
            print(f"Processing JAMS file {audio_file}")
            if ".jams" in audio_file.name:
                new_name = audio_file.name.replace(".jams", "")
                audio_file.rename(audio_file.parent / new_name)
                print(f"Renamed {audio_file} to {new_name}")


def reformat_audio_csv(partitions_path: Path) -> None:
    """
    Iterate over all the audio files in all the AUDIO partitions and rename
    files by removing the .jams string within the filename.
    Parameters
    ----------
    partitions_path : Path
        Path to the partitions.
    Returns
    -------
    None
    """
    for partition in partitions_path.iterdir():
        if partition.name not in AUDIO_PARTITIONS:
            continue
        print(f"Processing partition {partition.name}")

        audio_files_csv = partition / "choco" / "audio_files.csv"
        if partition.name == "schubert-winterreise":
            audio_files_csv = partition / "choco" / "audio" / "audio_files.csv"

        df = pd.read_csv(audio_files_csv)
        df["audio_file"] = (df["audio_file"].
                            apply(lambda x: str(x).
                                  replace(".jams", ".mp3")))
        df = df.sort_values(by=["jams_file"])
        df.to_csv(audio_files_csv, index=False)


if __name__ == '__main__':
    partitions_path = Path("../partitions")
    reformat_filenames(partitions_path)
    reformat_audio_csv(partitions_path)
