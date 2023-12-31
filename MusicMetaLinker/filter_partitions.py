"""
Filters for partitions based on the peculiarities of each repository.
"""

from pathlib import Path

from partitions_map import AUDIO_PARTITIONS, SCORE_PARTITIONS


def filter_partition(partition: Path,
                     limit: str | None) -> tuple[str | None, 
                                                 Path | None]:
    """
    Filter for the audio partitions.
    Parameters
    ----------
    partition : Path
        Path to the partition.
    limit : str | None
        Limit for the partition, accepts "audio", "score" or None.
    Returns
    -------
    partition_type : str
        Type of the partition, either "audio" or "score".
    partition : Path
        Path to the partition.
    """
    partition_type = None
    if partition.name in AUDIO_PARTITIONS:
        partition_type = "audio"
        if limit == "score":
            return partition_type, None
        elif partition.name == "schubert-winterreise":
            return (partition_type,
                    partition / "choco" / "audio" / "jams-converted")
    elif partition.name in SCORE_PARTITIONS:
        partition_type = "score"
        if limit == "audio":
            return partition_type, None
        if partition.name == "ireal-pro":
            if "ireal-pro-forum" in SCORE_PARTITIONS:
                return (partition_type,
                        partition / "choco" / "forum" / "jams-converted")
            if "ireal-pro-playlist" in SCORE_PARTITIONS:
                return (partition_type,
                        partition / "choco" / "playlists" / "jams")

    jams_path = partition / "choco" / "jams-converted"
    if jams_path.exists():
        return partition_type, jams_path
    return partition_type, partition / "choco" / "jams"
