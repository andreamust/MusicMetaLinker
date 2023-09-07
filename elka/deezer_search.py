"""
Script for searching songs on Deezer and getting the ID.
"""

import deezer

client = deezer.Client()

# Search for an artist
results = client.search(track='semaforo', artist='willie peyote', strict=False)
print(results[0].as_dict())
