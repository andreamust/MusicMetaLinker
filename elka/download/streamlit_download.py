"""

"""

import subprocess
import streamrip
from rip import core, config
# rip url https://www.deezer.com/us/track/1694424337 --directory="download"

# download from streamrip without command line

config = config.Config('config.toml')
config.load()

download = core.RipCore(config)
download.handle_urls(["https://www.deezer.com/us/track/1694424337"])
abc = download.download()


