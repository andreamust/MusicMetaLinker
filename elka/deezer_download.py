"""
Script for downloading songs from deezer.com
"""
import chunk

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from pydeezer import Deezer, util
from pydeezer.constants import track_formats

arl = "864f8f2176f4d97539ce2763a2d000ff25e93f76d37e0285791a9d3cac1dcea145f2643916e0fdb0372465736c9b09024641b989b4d66c207674c3502551bac354997c617e04c7833129926c73aa94be7c1459cc26a42af37409ec0720c7df27"
deezer = Deezer(arl=arl)
user_info = deezer.user
# or
# deezer = Deezer()
# user_info = deezer.login_via_arl(arl)

track = deezer.get_track("780587722")
data = deezer.get_track_download_url(track['info'], track_formats.FLAC, fallback=False)

print(deezer.get_track_valid_quality(track['info']))
deezer.download_track(track['info'],
                      quality=track_formats.MP3_320,
                      download_dir='./downloaded/',
                      filename='isophonic_777',
                      show_messages=False,
                      fallback=True,
                      progress_handler=None,
                      fallback_qualities=[track_formats.FLAC,
                                          track_formats.MP3_320,])





