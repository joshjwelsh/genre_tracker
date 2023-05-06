CREATE TABLE ingested_tracks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), -- internal id
    uri varchar NOT NULL UNIQUE, -- spotify uri
    user_id UUID NOT NULL, -- internal user id
    title VARCHAR NOT NULL, 
    artist VARCHAR NOT NULL, 
    album VARCHAR NOT NULL,
    album_id VARCHAR NOT NULL, -- spotify album id
    title_id VARCHAR NOT NULL, -- spotify track id
    artist_id VARCHAR NOT NULL, -- spotify artist id
    metadata JSON,
    source VARCHAR,
    timestamp TIMESTAMP, -- time when added to playlist
    ingested_at TIMESTAMP -- time when ingested
);