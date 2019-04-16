from cassandra.cluster import Cluster
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    # connect to default database

    try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect()
    except Exception as e: 
        print(e) 
    # create keyspace
    try: 
        session.execute(""" 
            CREATE KEYSPACE IF NOT EXISTS udacity  
            WITH REPLICATION =  
            { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }""" 
        ) 
    except Exception as e: 
        print(e)
        
    #Set KEYSPACE to the keyspace specified above
    try: 
        session.set_keyspace('udacity') 
    except Exception as e: 
        print(e) 
    
    return session, cluster


def drop_tables(session):
    for query in drop_table_queries:
        session.execute(query)


def create_tables(session):
    for query in create_table_queries:
        session.execute(query)


def main():
    session, cluster = create_database()
    
    drop_tables(session)
    create_tables(session)

    session.shutdown()
    cluster.shutdown()


if __name__ == "__main__":
    main()