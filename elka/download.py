"""
Script for downloading the dump from the MusicBrainz database.
"""

import argparse
import os
import sys
from urllib import request, error
import tqdm

class DownloadProgressBar(tqdm.tqdm):
    """
    Code taken from https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
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

    def __init__(self, url, output_dir):
        """Initializes the class."""
        # if no preferred server is specified, use the first one that responds
        if url is None:
            try:
                request.urlopen(self.url_server_1)
                self.url = self.url_server_1
                print('Using the first server.')
            except request.HTTPError:
                try:
                    request.urlopen(self.url_server_2)
                    self.url = self.url_server_2
                    print('Using the second server.')
                except request.HTTPError:
                    try:
                        request.urlopen(self.url_server_3)
                        self.url = self.url_server_3
                        print('Using the third server.')
                    except request.HTTPError as e:
                        raise error from e
        self.output_dir = output_dir

    def _get_latest_dump(self, file_name='mbdump.tar.bz2'):
        """Gets the latest dump from the MusicBrainz database."""
        try:
            print('Getting the latest dump from the MusicBrainz database...')
            # get latest dump
            latest_response = request.urlopen(self.url + 'LATEST')
            latest_dump = latest_response.read().decode('utf-8').strip()

            return self.url + latest_dump + '/' + file_name

        except Exception as e:
            raise error from e

    def download(self):
        """Downloads the dump from the MusicBrainz database."""
        download_url = self._get_latest_dump()

        try:
            print('Downloading the dump from the MusicBrainz database...')
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            with DownloadProgressBar(unit='B',
                                     unit_scale=True,
                                     miniters=1,
                                     desc='Downloading MusicBrainz dump') as dpb:
                request.urlretrieve(download_url,
                                    self.output_dir,
                                    reporthook=dpb.update_to)
            print('Download completed.')
        except Exception as e:
            raise error from e


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description='Download the dump from the MusicBrainz database.')
    # parser.add_argument('-u', '--url',
    #                     help='URL of the dump from the MusicBrainz database.')
    # parser.add_argument('-o', '--output_dir', help='Output directory.')
    # args = parser.parse_args()
    #
    # try:
    #     mb_download = MBDownload(args.url, args.output_dir)
    #     mb_download.download()
    # except DownloadError as e:
    #     print('Download failed.', file=sys.stderr)

    mb_download = MBDownload(None, 'data/dump.tar.bz2')
    download_path = mb_download.download()
