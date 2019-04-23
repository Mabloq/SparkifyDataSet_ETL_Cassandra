# Setup
## Prequisites
   - Must have python 3.x installed on your machine
   - Must have a local cassandra db installed on your machine
  
## Usage
   - In terminal, clone this github project and cd into the project folder Run these commands:
``` bash
  python create_tables.py
  python etl.py
```
   - The tabels will be autmatically created and populated with data read from the /event_data folder

# ETL Process doc
[Link to Excel Documentation](https://drive.google.com/file/d/1_IZwSWhPAeW_wq6ALj1MqqDE287HL0ch/view?usp=sharing)

## event_datafile_new.csv -> session_songplays table

Primary Key (session_id, session_item)

| Source Column                                 	| Source Data Type 	| Source Nullable 	| Transformation 	| Destination Column       	| Dest. Data Type                                               	| Dest. Nullable 	|
|---------------------------------------------------|------------------	|-----------------	|----------------	|--------------------------	|---------------------------------------------------------------	|----------------	|
| line[8]                                       	| string           	| no              	| cast to int    	| session_id               	| smallint                                                      	| no             	|
| line[3]                                       	| string           	| no              	| cast to int    	| session_item             	| smallint                                                      	| no             	|
| line[0]                                       	| sting            	| no              	|                	| artist                   	| text                                                          	| no             	|
| line[9]                                       	| string           	| no              	|                	| song_title               	| text                                                          	| no             	|
| line[5]                                       	| string           	| no              	| cast to float  	| length                   	| double                                                        	| no             	|

## event_datafile_new.csv -> song_songplays table

Primary Key (song_title, user_id)

| Source Column                                 	| Source Data Type 	| Source Nullable 	| Transformation 	| Destination Column       	| Dest. Data Type                                               	| Dest. Nullable 	|
|---------------------------------------------------|------------------	|-----------------	|----------------	|--------------------------	|---------------------------------------------------------------	|----------------	|
| line[8]                                       	| string           	| no              	| cast to int    	| session_id               	| smallint                                                      	| NO             	|
| line[3]                                       	| string           	| no              	| cast to int    	| session_item             	| smallint                                                      	| NO             	|
| line[0]                                       	| string           	| yes             	|                	| artist                   	| text                                                          	| NO             	|
| line[9]                                       	| string           	| yes             	|                	| song_title               	| text                                                          	| NO             	|
| line[1]                                       	| string           	|                 	|                	| first_name               	| text                                                          	| NO             	|
| line[4]                                       	| string           	| yes             	|                	| last_name                	| text                                                          	| NO             	|

## event_datafile_new.csv -> user_songplays table

Primary Key (user_id, session_id, session_item)

| Source Column                                 	| Source Data Type 	| Source Nullable 	| Transformation 	| Destination Column       	| Dest. Data Type                                               	| Dest. Nullable 	|
|---------------------------------------------------|------------------	|-----------------	|----------------	|--------------------------	|---------------------------------------------------------------	|----------------	|
| line[10]                                      	| string           	| no              	| cast to int    	| user_id                  	| smallint                                                      	| NO             	|
| line[0]                                       	| string           	| no              	|                	| artist                   	| text                                                          	| NO             	|
| line[9]                                       	| string           	| no              	|                	| song_title               	| text                                                          	| NO             	|
| line[1]                                       	| string           	| no              	|                	| first_name               	| text                                                          	| NO             	|
| line[4]                                       	| string           	| no              	|                	| last_name                	| text                                                          	| NO             	|

# Data Modeling Justifcations
## Table 1: session_songplays

 - For our session_songplays table we model it so that we can support the following query:

    ``` sql
        Select artist, song_title, length
        from session_songplays
        where session_id = 338 and session_item = 4
        
    ```
    ...
 - We see in our query that we are filtering first by session_id and then by session_item.
 - Therefore session_id (being unique) becomes our candidate for our PRIMARY KEY and session_item becomes a good choice for a clustering column
   in order to support the query defined above.
   
## Table 2: user_songplays

 - For our user_songplays table we model it so that we can support the following query:

    ``` sql
        Select artist, song_title (sorted by session_item), first_name, last_name
        from session_songplays
        where user_id = 10 and session_id = 182
        
    ```
    ...
 - We see in our query that we are filtering first by user_id and then by session_id.
 - Therefore user_id (being unique and supporting our query) becomes our candidate for our PRIMARY KEY and session_id becomes a good choice 
   for a clustering column in order to support the query defined above.
 - However we must note that the query also has the requirement that the artist, song_title fields must be sorted by session_item 
 - Therefore we had a second clustering column session_item
 
## Table 3: song_songplays
 - For our song_songplays table we model it so that we can support the following query:

    ``` sql
        SELECT first_name, last_name 
        from song_songplays 
        WHERE song_title='All Hands Against His Own'
        
    ```
    ...
 - We see in our query that we are filtering first by song_title
 - song_title (not being unique) makes it a bad candidate for our PRIMARY KEY by itself
 - Therfore we Create a compound primary key with user_id, this way we can see if more than one person listened to this song, what are there
   distinct names and membership level etc.
 - Note: If one wanted more granular information, then a 3 column primary key could be created that would include an added session_id which would
   enable us to know more about the context in which a group of users listened to a specific song (what other songs did they play in the session
   ,in how many distinct sessions did a user listen to a song etc.)