import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from db import DBManager
from env import CLIENT_ID, CLIENT_SECRET

# Replace these values with your own credentials
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
redirect_uri = "http://localhost:4000/callback"

class IngestedTrack:
    def __init__(self, uri, title, artist, album, album_id, title_id, artist_id, metadata, source, timestamp, ingested_at):
        self.title = title
        self.artist = artist
        self.album = album
        self.album_id = album_id
        self.title_id = title_id
        self.artist_id = artist_id
        self.metadata = metadata
        self.source = source
        self.timestamp = timestamp
        self.ingested_at = ingested_at
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

def get_artist_genre(artist_id):
    artist = sp.artist(artist_id)
    return ', '.join(artist['genres'])


# Function to fetch and print liked songs
def collect_songs():
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
            title = track['name']
            ingested_at = datetime.now()
            artist = track['artists'][0]['name']
            artist_id = track['artists'][0]['id']
            album = track['album']['name']
            album_id = track['album']['id']
            title_id = track['id']
            source = 'spotify'
            metadata = track 
            uri = track['uri']
            ingested_track = IngestedTrack(uri, title, artist, album, album_id, title_id, artist_id, metadata, source, timestamp, ingested_at)
            db = DBManager()
            db.insert(ingested_track)


        # Increment the offset for the next batch of songs
        offset += len(results["items"])

