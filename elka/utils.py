"""
Utility functions for the elka package.
"""

from pathlib import Path

import pandas as pd


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
