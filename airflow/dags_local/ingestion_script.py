import pandas as pd
# pandas can connect with sql databases to produce sql dialect specific results, using sqlalchemy engines
from sqlalchemy import create_engine

import time

def ingest_callable(user, password, host, port, db, table_name, csv_file):
    
    print(table_name, csv_file)
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}') # creating and connecting to the postgres database
    engine.connect()
    
    print('Connection established successfully!')

    # iterator allows us to chunk parts of data into batches. Large data doesn't fit in memory, batching to chunks is useful in data engg
    raw_data_iter = pd.read_csv(csv_file, compression='gzip', iterator=True, chunksize=100000) # returns a generator useful for batching

    raw_data_df = next(raw_data_iter)

    # thanks to sqlalchemy and pandas integration, we have an api to execute sql eqv code 
    # the n=0 is there to select only the head (column names) of the df. Effectively, this creates a table with the columns

    raw_data_df.tpep_pickup_datetime = pd.to_datetime(raw_data_df.tpep_pickup_datetime)
    raw_data_df.tpep_dropoff_datetime = pd.to_datetime(raw_data_df.tpep_dropoff_datetime)
    headers = raw_data_df.head(n=0)

    headers.to_sql(name=table_name, con=engine, if_exists='replace')
    raw_data_df.tpep_pickup_datetime = pd.to_datetime(raw_data_df.tpep_pickup_datetime)
    raw_data_df.tpep_dropoff_datetime = pd.to_datetime(raw_data_df.tpep_dropoff_datetime)
    raw_data_df.to_sql(name=table_name, con=engine, if_exists='append')


    for dataframe in raw_data_iter:
        start = time.time()
        dataframe.tpep_pickup_datetime = pd.to_datetime(dataframe.tpep_pickup_datetime)
        dataframe.tpep_dropoff_datetime = pd.to_datetime(dataframe.tpep_dropoff_datetime)
        dataframe.to_sql(name=table_name, con=engine, if_exists='append')
        print("Inserted chunk, time taken:", time.time()-start,"sec")