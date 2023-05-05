import psycopg2
from env import POSTGRES_CONNECTION_STRING, JOSH_UUID
import json
# Define the connection string


class DBManager:
	conn_string = POSTGRES_CONNECTION_STRING
	def __init__(self):
                # Try to connect to the database
		try:
			self.conn = psycopg2.connect(self.conn_string)
			print("Connection successful!")
		except psycopg2.Error as e:
			print("Unable to connect to database:", e)

	def select(self):
		# Define a query to execute
		query = "SELECT * FROM ingested_tracks;"
		try:
			cur = self.conn.cursor()
			cur.execute(query)
			results = cur.fetchall()
			print("Query results:", results)
		except psycopg2.Error as e:
			print("Error executing query:", e)
	
	def insert(self, ingested_tracklist):
		# Define a query to execute
		metadata = ingested_tracklist.metadata
		blob = json.dumps(metadata)
		query = f"""INSERT INTO ingested_tracks (title, user_id, timestamp, added_at, artist, album, source, metadata, uri) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""


		try:
			cur = self.conn.cursor()
			cur.execute(query, (ingested_tracklist.title, JOSH_UUID, ingested_tracklist.timestamp, ingested_tracklist.added_at, ingested_tracklist.artist, ingested_tracklist.album, ingested_tracklist.source, blob, ingested_tracklist.uri))
			self.conn.commit()
			print("Query executed successfully!")
		except psycopg2.Error as e:
			print("Error executing query:", e)
			print(query)
			input()

