# enrich data with genre information
# store transformed data in table 'tracks_normalized' in database vertzy

from sp import collect_songs, get_artist_genre
from db import DBManager
import pandas as pd 

def create_staging_genre_table():
   db = DBManager()
   ids = db.select_all_artist_id()
   for id in ids:
        artist_id = id[0]
        genres = get_artist_genre(artist_id)
        db.insert_stage_genre(artist_id, genres)


# Only run once to initiate the table 
def create_daily_ranking():
    statement = f"""
    CREATE TABLE IF NOT EXISTS top_genres_per_day AS
    WITH genre_counts AS (
                SELECT
                        date,
                        genre,
                        COUNT(*) AS count
                FROM (
                        SELECT
                                it.timestamp::date AS date,
                                UNNEST(string_to_array(sg.genre, ', ')) AS genre
                        FROM 
                                ingested_tracks AS it
                        JOIN 
                                stage_genres AS sg 
                        ON it.artist_id = sg.artist_id
                ) AS genres_unnested
                GROUP BY 
                        date, 
                        genre
        ),
        ranked_genres AS (
                SELECT
                        date,
                        genre,
                        count,
                        RANK() OVER (PARTITION BY date ORDER BY count DESC) AS rank
                FROM 
                        genre_counts
        )
        SELECT
                date,
                genre,
                count
        FROM 
                ranked_genres
        WHERE 
                rank = 1;
        """
    db = DBManager()
    db.__execute__(statement)


# This pipeline is expected to work for a single user. 
# If you want to try for another use you need to delete the data, including tables, in the database first.
# Schedule this pipeline to run once
def single_user_pipeline():
        collect_songs()
        create_staging_genre_table()
        create_daily_ranking()



single_user_pipeline()