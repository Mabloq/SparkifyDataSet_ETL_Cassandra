import pandas as pd
from cassandra.cluster import Cluster
import re
import os
import glob
import json
import csv
from sql_queries import *


def gen_filepaths():
    """
    crawls the /event_data directory and returns a python list of filepaths for each csv file found
    
    Returns:
    file_path_list list:list of json data
    """
    # Get your current folder and subfolder event data
    filepath = os.getcwd() + '/event_data'

    # Create a for loop to create a list of files and collect each filepath
    for root, dirs, files in os.walk(filepath):
        # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root,'*'))
    
    return file_path_list

def gen_csv(filepaths):
    """
    generates one unified csv file ("event_datafile_new.csv") with all the row data from each csv found in /event_data directory

    Parameters:
        filepaths (list[str]): list of string type filepath of each song json doc
    
    """
    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = [] 

    # for every filepath in the file path list 
    for f in filepaths:
        # reading csv file 
        with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            next(csvreader)

            # extracting each data row one by one and append it        
            for line in csvreader:
                #print(line)
                full_data_rows_list.append(line) 

    # creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
    # Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                    'level','location','sessionId','song','userId'])
        for row in full_data_rows_list:
            #if fists item in row is empty then its just the logout or home page, we dont need these eows
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))

def process_sessions(session, file):
    """
    Strategy pattern like function passed into process_data function, used to transform "event_datafile_new.csv" file
    into appropriate format and then insert into session_songplays table

    Parameters:
        session (object): live keyspace cassandra session used to execute insert query
        file (str): filepath to event_data_new.csv
    """
    with open(file, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for line in csvreader:
            #line = ['artist','firstName','gender','itemInSession','lastName','length','level','location','sessionId','song','userId']
            session.execute(session_insert, (int(line[8]), int(line[3]), line[0], line[9], float(line[5])))
            
            
def process_users(session, file):
    """
    Strategy pattern like function passed into process_data function, used to transform "event_datafile_new.csv" file
    into appropriate format and then insert into user_songplays table

    Parameters:
        session (object): live keyspace cassandra session used to execute insert query
        file (str): filepath to event_data_new.csv
    """
    with open(file, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for line in csvreader:
            #line = ['artist','firstName','gender','itemInSession','lastName','length','level','location','sessionId','song','userId']
            session.execute(users_insert, (int(line[10]), int(line[8]), int(line[3]), line[0], line[9], line[1], line[4]))

            
def process_songs(session, file):
    """
    Strategy pattern like function passed into process_data function, used to transform "event_datafile_new.csv" file
    into appropriate format and then insert into song_songplays table

    Parameters:
        session (object): live keyspace cassandra session used to execute insert query
        file (str): filepath to event_data_new.csv
    """
    with open(file, encoding = 'utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader) # skip header
        for line in csvreader:
            #line = ['artist','firstName','gender','itemInSession','lastName','length','level','location','sessionId','song','userId']
            session.execute(songs_insert, (int(line[10]), line[0], line[9], line[1], line[4]))

        
def process_data(session, func, query):
    """
    Strategy pattern like function that takes a particular func argument to process and insert different types of data
    into diffrent types of tables in our keyspace

    Parameters:
        session (object): live keyspace cassandra session used to execute insert query
        file (str): filepath to event_data_new.csv
    """
    file = 'event_datafile_new.csv'
    func(session, file)
    print('done')
    print('Test query: ')
    test_completion(session, query)
   

def test_completion(session, query):
    """
    After each table creation and insertion we run a test query

    Parameters:
        session (object): live keyspace cassandra session used to execute insert query
        query (str): test query to prove our insertions worked    
    """
    rows = session.execute(query)
    for row in rows:
        print(row)

def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('udacity') 
    filepaths = gen_filepaths()
    #generate csv to copy int apache
    gen_csv(filepaths)
    print("==============================================================")
    print('processing session_songplays table...')
    process_data(session, process_sessions, session_query)
    print("==============================================================")
    print('processing user_songplays table...')
    process_data(session, process_users, user_query)
    print("==============================================================")
    print('processing song_songplays table..')
    process_data(session, process_songs, song_query)
    print("==============================================================")
        
if __name__ == "__main__":
    main()

