PRAGMA foreign_keys = ON;

CREATE TABLE artist (
  artist_id     INTEGER PRIMARY KEY,
  name          TEXT NOT NULL UNIQUE
);

CREATE TABLE album (
  album_id      INTEGER PRIMARY KEY,
  artist_id     INTEGER NOT NULL,
  title         TEXT NOT NULL,
  release_year  INTEGER,
  
  UNIQUE (artist_id, title),
  FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE CASCADE
);

CREATE TABLE song (
  song_id       INTEGER PRIMARY KEY,
  album_id      INTEGER NOT NULL,
  title         TEXT NOT NULL,
  track_number  INTEGER NOT NULL,
 
  CHECK (track_number > 0),
  CHECK (length_sec > 0),

  UNIQUE (album_id, track_number),
  FOREIGN KEY (album_id) REFERENCES album(album_id) ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS idx_album_artist ON album(artist_id);
CREATE INDEX IF NOT EXISTS idx_song_album ON song(album_id);

