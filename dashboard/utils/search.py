# shows artist info for a URN or URL

import spotipy
import sys
import pprint

if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    search_str = 'skakira'

token = 'xxx'

sp = spotipy.Spotify(auth=token)
result = sp.search(q=search_str, type='artist')
print(result)
#pprint.pprint(result)
