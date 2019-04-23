# drop tables
drop_sessions = "DROP TABLE IF EXISTS session_songplays"
drop_users = "DROP TABLE IF EXISTS user_songplays"
drop_songs = "DROP TABLE IF EXISTS songs_songplays"

# create tables
create_sessions = """
    CREATE TABLE IF NOT EXISTS session_songplays
        (session_id smallint,
         session_item smallint, 
         artist text, 
         song_title text, 
         length double, 
         PRIMARY KEY (session_id, session_item)
         )
"""

create_users = """
    CREATE TABLE IF NOT EXISTS user_songplays 
        (user_id smallint, 
         session_id smallint,
         session_item smallint,
         artist text,
         song_title text,
         first_name text,
         last_name text,
         PRIMARY KEY (user_id, session_id, session_item)
         )
"""

create_songs = """
    CREATE TABLE IF NOT EXISTS song_songplays
        (user_id smallint, 
         artist text,
         song_title text,
         first_name text,
         last_name text,
         PRIMARY KEY (song_title, user_id)
        )
"""

# inserts
session_insert = """
    INSERT INTO session_songplays 
        (session_id, 
         session_item, 
         artist, 
         song_title, 
         length
         )
    VALUES (%s, %s, %s, %s, %s)
"""

users_insert = """
    INSERT INTO user_songplays
        (user_id, 
         session_id, 
         session_item, 
         artist, 
         song_title, 
         first_name, 
         last_name
         )
     VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

songs_insert = """
    INSERT INTO song_songplays 
        (user_id, artist, 
         song_title, 
         first_name, 
         last_name
         )
    VALUES (%s, %s, %s, %s, %s)
"""
# test queries

session_query = "SELECT artist, song_title, length FROM session_songplays WHERE session_id=338 AND session_item =4"
user_query = "SELECT artist, song_title, first_name, last_name FROM user_songplays WHERE user_id = 10 and session_id = 182"
song_query = "SELECT first_name, last_name FROM song_songplays WHERE song_title='All Hands Against His Own'"

# package them

drop_table_queries = [drop_sessions, drop_users, drop_songs]
create_table_queries = [create_sessions, create_users, create_songs]
table_inserts = [session_insert, users_insert, songs_insert]
test_queries = [session_query, user_query, song_query]