"""
Linking module for AcousticBrainz data.
"""

import requests


def acousticbrainz_link(mbid: str) -> str | None:
    """
    Script for checking if the acousticbrainz resource exists. If it does,
    returns the link to the resource. Otherwise, returns None.
    Parameters
    ----------
    mbid : str
        MusicBrainz ID.
    Returns
    -------
    str
        AcousticBrainz link.
    """
    url = f"https://acousticbrainz.org/{mbid}"
    response = requests.get(url)
    if response.status_code == 200:
        return url
    return None


if __name__ == "__main__":
    # test the function
    print(acousticbrainz_link("706be20f-e062-4569-94cc-25842dc0a625"))
