# MusicMetaLinker

MusicMetaLinker is a Python library designed to seamlessly link music tracks to external sources, enhancing your music collection with rich and accurate metadata. With MusicMetaLinker, you can effortlessly connect your music metadata, such as artist names, track names, albums, durations, track numbers, ICRC codes, and MusicBrainz IDs, to external music databases and services. MusicMetaLinker currently supports four linkers: MusicBrainz, AcousticBrainz, YouTube Music, and Deezer.

## Installation

You can install the latest version of MusicMetaLinker by cloning this repository and running the following command:

```bash
pip install git+https://github.com/andreamust/MusicMetaLinker.git
```

## Usage
Using MusicMetaLinker is straightforward. Import the library into your Python script and use it to link your music metadata to external sources. Here's a basic example:

```python
from MusicMetaLinker.linking import linking

# Create a linking object
linker = linking.Align(
                artist="The Beatles",
                album="Let It Be",
                track="Let It Be",
                track_number=4,
                duration=168.25,
                release_year=1970,
                musicbrainz_id="b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d",
                isrc="GBAYE0601690",
                strict=False,
            )
# Link the metadata
track_name = linker.get_track()
artist_name = linker.get_artist()
album_name = linker.get_album()
track_number = linker.get_track_number()
duration = linker.get_duration()
release_year = linker.get_release_date()
isrc = linker.get_isrc()

# Get the identifiers
links = {'musicbrainz': linker.get_mbid(),
         'isrc': linker.get_isrc() if isrc is None else isrc,
         'deezer': linker.get_deezer_id(),
         'deezer_url': linker.get_deezer_link(),
         'youtube_url': linker.get_youtube_link(),
         }
```

Of course, in the example above, the linker works with very little metadata, such as the sole artist name, and track name.
At the same time, it is possible to query only using a single identifier, such as the MusicBrainz ID, the ISRC, or the Deezer ID. For example:

```python
from MusicMetaLinker.linking import linking

# Create a linking object
linker = linking.Align(
                musicbrainz_id="b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d",
            )
```

## Workflow
MusicMetaLinker follows a three-step workflow to link music track metadata to external sources:

1. **Service Selection**: MusicMetaLinker evaluates the available metadata and selects the most suitable external service (e.g., MusicBrainz, AcousticBrainz, YouTube Music, Deezer) to extract accurate information.

2. **Information Retrieval**: MusicMetaLinker connects to the chosen service's API, searches for the best match based on the provided metadata, and retrieves detailed information about the music track.

3. **Filtering and Return**: MusicMetaLinker filters the retrieved information to find the best match for the given metadata. It returns all the relevant metadata found, enhancing your music tracks with external data.

Additionally, MusicMetaLinker can process directories of music files (jams files), read their metadata, and rewrite new jams files with the retrieved links, ensuring your music collection remains organized and enriched.


## License
MIT License

Copyright (c) 2023 Andrea Poltronieri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
