import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from db import DBManager

# Replace these values with your own credentials
client_id = "bdf42dbf94f6444e90cccb0c6da0360a"
client_secret = "0a5ece4316504b12827fd266330b8be3"
redirect_uri = "http://localhost:4000/callback"

class IngestedTrack:
    def __init__(self, title, timestamp, added_at, artist, album, source, metadata, uri):
        self.title = title
        self.timestamp = timestamp
        self.added_at = added_at
        self.artist = artist
        self.album = album
        self.source = source
        self.metadata = metadata
        self.uri = uri

    def __repr__(self):
        return f"{self.name} by {self.artist} from {self.source}"

    def __str__(self):
        return f"{self.name} by {self.artist} from {self.source}"


# Set up the spotipy client with the necessary credentials
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-library-read",
    )
)

# Function to fetch and print liked songs
def print_liked_songs():
    # Initialize the offset for pagination
    offset = 0

    while True:
        # Fetch a batch of liked songs
        results = sp.current_user_saved_tracks(limit=20, offset=offset)

        # Check if there are no more songs
        if not results["items"]:
            break

        # Iterate over the songs and print their names
        for item in results["items"]:
            timestamp = item["added_at"]
            track = item["track"]
            print(f"{track['name']}")
            title = track['name']
            added_at = datetime.now()
            artist = track['artists'][0]['name']
            album = track['album']['name']
            source = 'spotify'
            metadata = track 
            uri = track['uri']
            ingested_track = IngestedTrack(title, timestamp, added_at, artist, album, source, metadata, uri)
            db = DBManager()
            db.insert(ingested_track)

        

        # Increment the offset for the next batch of songs
        offset += len(results["items"])

# Call the function to print liked songs
print_liked_songs()
