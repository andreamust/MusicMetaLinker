"""Script for extracting relevant information from the JAMS files that
will be used for aligning the data with the MusicBrainz database.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import tqdm

from elka import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_jams(jams_file: Path, output_dir: Path) -> None:
    pass
