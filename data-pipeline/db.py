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
	
	def insert(self, ingested_track):
		# Define a query to execute
		metadata = ingested_track.metadata
		blob = json.dumps(metadata)
		query = f"""INSERT INTO ingested_tracks (title, artist, album, album_id, title_id, artist_id, metadata, source, timestamp, ingested_at, uri, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s) ON CONFLICT DO NOTHING;"""

		try:
			cur = self.conn.cursor()
			cur.execute(query, (ingested_track.title, ingested_track.artist, ingested_track.album, ingested_track.album_id, ingested_track.title_id, ingested_track.artist_id, blob, ingested_track.source, ingested_track.timestamp, ingested_track.ingested_at, ingested_track.uri, JOSH_UUID))
			self.conn.commit()
			print("Query executed successfully!")
		except psycopg2.Error as e:
			print("Error executing query:", e)
			print(query)
			input()

	def select_all_artist_id(self):
		# Define a query to execute
		query = "SELECT distinct(artist_id) FROM ingested_tracks;"
		try:
			cur = self.conn.cursor()
			cur.execute(query)
			results = cur.fetchall()
			return results
		except psycopg2.Error as e:
			print("Error executing query:", e)

	def insert_stage_genre(self,artist_id, genres):

		query = f"""INSERT INTO stage_genres (artist_id, genre) VALUES (%s, %s) ON CONFLICT DO NOTHING;"""
		try: 
			cur = self.conn.cursor()
			cur.execute(query, (artist_id, genres))
			self.conn.commit()
			print("Query executed successfully!")
		except psycopg2.Error as e:
			print("Error executing query:", e)
			print(query)
			input()
		     
	
	def select_filter(self, query):
		try:
			cur = self.conn.cursor()
			cur.execute(query)
			results = cur.fetchall()
			return results
		except psycopg2.Error as e:
			print("Error executing query:", e)
			print(query)
			input()
	
	def __execute__(self, query):

		try:
			cur = self.conn.cursor()
			cur.execute(query)
			self.conn.commit()
			print("Query executed successfully!")
		except psycopg2.Error as e:
			print("Error executing query:", e)
			print(query)
			input()