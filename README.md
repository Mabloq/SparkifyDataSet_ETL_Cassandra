# Setup
#Prequisites
   - Must have python 3.x installed on your machine
   - Must have a local cassandra db installed on your machine
  
#Usage
   - In terminal, clone this github project and cd into the project folder Run these commands:
``` bash
  python create_tables.py
  python etl.py
```
   - The tabels will be autmatically created and populated with data read from the /event_data folder

# ETL Process doc
[Link to Excel Documentation](https://drive.google.com/file/d/1_IZwSWhPAeW_wq6ALj1MqqDE287HL0ch/view?usp=sharing)
##csv -> session_songplays table
| Source Column                                 	| Source Data Type 	| Source Nullable 	| Transformation 	| Destination Column       	| Dest. Data Type                                               	| Dest. Nullable 	|
|---------------------------------------------------|------------------	|-----------------	|----------------	|--------------------------	|---------------------------------------------------------------	|----------------	|
|event_datafile_new.csv           	                |                  	|                 	|                	| Table: session_songplays 	| Primary Key:  PRIMARY KEY (session_id, session_item)          	|                	|
| line[8]                                       	| string           	| no              	| cast to int    	| session_id               	| smallint                                                      	| no             	|
| line[3]                                       	| string           	| no              	| cast to int    	| session_item             	| smallint                                                      	| no             	|
| line[0]                                       	| sting            	| no              	|                	| artist                   	| text                                                          	| no             	|
| line[9]                                       	| string           	| no              	|                	| song_title               	| text                                                          	| no             	|
| line[5]                                       	| string           	| no              	| cast to float  	| length                   	| double                                                        	| no             	|

##csv -> song_songplays table

| Source Column                                 	| Source Data Type 	| Source Nullable 	| Transformation 	| Destination Column       	| Dest. Data Type                                               	| Dest. Nullable 	|
|---------------------------------------------------|------------------	|-----------------	|----------------	|--------------------------	|---------------------------------------------------------------	|----------------	|
| event_datafile_new.csv           	                |                  	|                 	|                	| Table: song_songplays    	| Primary Key:  PRIMARY KEY (song_title, artist)                	|                	|
| line[8]                                       	| string           	| no              	| cast to int    	| session_id               	| smallint                                                      	| NO             	|
| line[3]                                       	| string           	| no              	| cast to int    	| session_item             	| smallint                                                      	| NO             	|
| line[0]                                       	| string           	| yes             	|                	| artist                   	| text                                                          	| NO             	|
| line[9]                                       	| string           	| yes             	|                	| song_title               	| text                                                          	| NO             	|
| line[1]                                       	| string           	|                 	|                	| first_name               	| text                                                          	| NO             	|
| line[4]                                       	| string           	| yes             	|                	| last_name                	| text                                                          	| NO             	|

##csv -> user_songplays table

| Source Column                                 	| Source Data Type 	| Source Nullable 	| Transformation 	| Destination Column       	| Dest. Data Type                                               	| Dest. Nullable 	|
|---------------------------------------------------|------------------	|-----------------	|----------------	|--------------------------	|---------------------------------------------------------------	|----------------	|
| event_datafile_new.csv                            |                  	|                 	|                	| Table: user_songplays    	| Primary Key:  PRIMARY KEY (user_id, session_id, session_item) 	|                	|
| line[10]                                      	| string           	| no              	| cast to int    	| user_id                  	| smallint                                                      	| NO             	|
| line[0]                                       	| string           	| no              	|                	| artist                   	| text                                                          	| NO             	|
| line[9]                                       	| string           	| no              	|                	| song_title               	| text                                                          	| NO             	|
| line[1]                                       	| string           	| no              	|                	| first_name               	| text                                                          	| NO             	|
| line[4]                                       	| string           	| no              	|                	| last_name                	| text                                                          	| NO             	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|
|                                               	|                  	|                 	|                	|                          	|                                                               	|                	|