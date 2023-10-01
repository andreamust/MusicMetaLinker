"""
Scripts for preparing the dataset. It creates the dataset by adding all the 
partitions to the same folder and creating the metadata file.
"""

import argparse
import logging
import os
from pathlib import Path
from filter_partitions import filter_partition

import pandas as pd


BASE_PATH = Path(__file__).parent.parent / "partitions"

logging.basicConfig(filename='./prepare_dataset.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

logger = logging.getLogger('prepare_dataset')


def prepare_schubert(output_path: str | Path) -> None:
    """
    """
    # define the paths
    output_path = Path(output_path)
    meta_score_path = BASE_PATH / "schubert-winterreise" / "choco" / "score" / "meta.csv"
    meta_audio_path = BASE_PATH / "schubert-winterreise" / "choco" / "audio" / "meta.csv"
    # get the metadata
    meta_score = pd.read_csv(meta_score_path)
    meta_audio = pd.read_csv(meta_audio_path)
    # create the output folder if it does not exist
    output_path.mkdir(parents=True, exist_ok=True)

    for score_file in meta_score["id"]:
        score_id = meta_score[meta_score["id"] ==
                              score_file]["score_file"].values[0]
        audio_id = meta_audio[meta_audio["track_file"].str.contains(
            score_id)]["id"].values

        # define score path
        score_path_original = BASE_PATH / "schubert-winterreise" / \
            "choco" / "score" / "jams" / (score_file + ".jams")

        # for each audio file, create a copy of the score file with the same name
        for audio_file in audio_id:
            # define the paths
            audio_path = BASE_PATH / "schubert-winterreise" / \
                "choco" / "audio" / "audio" / (audio_file + ".flac")
            score_path_copy = output_path / (audio_file + ".jams")
            print(score_path_copy)
            print(audio_path)
            # check that the audio file exists
            if audio_path.exists():
                # copy the score file
                os.system(f"cp {score_path_original} {score_path_copy}")


def prepare_dataset(output_path: str | Path,
                    limit: str | None = None) -> None:
    """
    Prepares the dataset by adding all the partitions to the same folder and
    creating the metadata file.
    Returns
    -------
    None
    """
    # define paths and create folders
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    # jams path
    jams_path = output_path / "jams"
    jams_path.mkdir(parents=True, exist_ok=True)
    # audio path
    audio_path = output_path / "audio"
    audio_path.mkdir(parents=True, exist_ok=True)
    # metadata path
    metadata_path = output_path / "metadata.csv"

    # create the metadata file
    metadata = pd.DataFrame(index=None)

    for partition in BASE_PATH.iterdir():
        partition_type, partition_path = filter_partition(partition, limit)
        if not partition_type or not partition_path:
            continue
        logger.info(f"Processing {partition_path}")
        jams_files = partition_path.glob("*.jams")
        audio_files = (partition_path.parent / "audio").glob("*.flac")
        metadata_file = partition_path.parent / "audio_files.csv"

        # copy all the jams_files to the jams folder
        for jams_file in jams_files:
            os.system(f"cp {jams_file} {jams_path}")

        # copy all the audio files to the audio folder
        for audio_file in audio_files:
            print(audio_file)
            os.system(f"cp {audio_file} {audio_path}")

        # add the metadata to the metadata file
        meta = pd.read_csv(metadata_file)
        metadata = pd.concat([meta, metadata], ignore_index=True)

    # save the metadata file
    metadata.to_csv(metadata_path)
        
        
if __name__ == "__main__":
    prepare_dataset("./audio_partitions", limit="audio")
