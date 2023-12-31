"""
Script for downloading the dump from the MusicBrainz database.
"""
import argparse
import logging
import os
import sys
import tarfile
from pathlib import Path
from urllib import request, error

import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DownloadProgressBar(tqdm.tqdm):
    """
    Class for displaying the progress bar while downloading the dump from the
    """

    def update_to(self, chunk_id=1, max_chunk_size=1, total_size=None):
        if total_size is not None:
            self.total = total_size
        self.update(chunk_id * max_chunk_size - self.n)


class MBDownload:
    """Class for downloading the dump from the MusicBrainz database."""

    url_server_1 = 'https://data.metabrainz.org/pub/musicbrainz/data/fullexport/'
    url_server_2 = 'https://ftp.osuosl.org/pub/musicbrainz/data/fullexport/'
    url_server_3 = 'https://mirrors.dotsrc.org/MusicBrainz/data/fullexport/'

    def __init__(self, url: None | str,
                 output_dir: str | Path,
                 clean: bool) -> None:
        """
        Initializes the class.

        Parameters
        ----------
        url : str | None
            URL of the dump from the MusicBrainz database. If not specified,
            the first server that responds is used.
        output_dir : str
            Output directory where the dump will be downloaded.
        clean : bool
            If True, the compressed data will be removed after extraction.

        Raises
        ------
        urllib.error.HTTPError
            If the specified URL is not valid.

        Returns
        -------
        None
        """
        # if no preferred server is specified, use the first one that responds
        if url is None:
            try:
                request.urlopen(self.url_server_1)
                self.url = self.url_server_1
                logger.info('Using the first server.')
            except request.HTTPError:
                try:
                    request.urlopen(self.url_server_2)
                    self.url = self.url_server_2
                    logger.info('Using the second server.')
                except request.HTTPError:
                    try:
                        request.urlopen(self.url_server_3)
                        self.url = self.url_server_3
                        logger.info('Using the third server.')
                    except request.HTTPError as e:
                        raise error from e
        self.output_dir = output_dir
        self.file_name = 'mbdump.tar.bz2'

    def _get_latest_dump(self, file_name: str = 'mbdump.tar.bz2') -> str:
        """
        Gets the latest dump from the MusicBrainz database.

        Parameters
        ----------
        file_name : str
            Name of the dump file.

        Raises
        ------
        urllib.error.HTTPError
            If the specified URL is not valid.

        Returns
        -------
        str
            URL of the latest dump.
        """

        self.file_name = file_name

        try:
            logger.info('Getting the latest dump from MusicBrainz...')
            # get latest dump
            latest_response = request.urlopen(self.url + 'LATEST')
            latest_dump = latest_response.read().decode('utf-8').strip()

            return self.url + latest_dump + '/' + file_name

        except Exception as e:
            logger.error('Getting the latest dump failed.')
            raise error from e

    def download(self):
        """
        Downloads the dump from the MusicBrainz database.

        Raises
        ------
        urllib.error.HTTPError
            If the specified URL is not valid.

        Returns
        -------
        None
        """
        download_url = self._get_latest_dump()

        compressed_file = self.output_dir + self.file_name

        try:
            logger.info('Downloading the dump from MusicBrainz...')
            # download the dump
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            with DownloadProgressBar(unit='B',
                                     unit_scale=True,
                                     miniters=1,
                                     desc='Downloading MusicBrainz') as dpb:
                request.urlretrieve(download_url,
                                    compressed_file,
                                    reporthook=dpb.update_to)
            logger.info('Download finished.')

            # extract the dump
            logger.info('Extracting the dump...')
            tar = tarfile.open(compressed_file, 'r:bz2')
            tar.extractall(self.output_dir)
            tar.close()
            logger.info('Extraction finished.')
        except Exception as e:
            logger.error('Download failed.')
            raise error from e


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download the dump from the MusicBrainz database.')
    parser.add_argument('-u', '--url',
                        help='URL of the dump from the MusicBrainz database.')
    parser.add_argument('-o', '--output_dir', help='Output directory.')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='If True, the compressed data will be removed '
                             'after extraction.')
    args = parser.parse_args()

    try:
        mb_download = MBDownload(args.url, args.output_dir, args.clean)
        mb_download.download()
    except error as e:
        print('Download failed.', file=sys.stderr)
