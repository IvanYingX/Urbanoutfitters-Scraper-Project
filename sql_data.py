from sqlalchemy import create_engine
import pandas as pd

def sql_data(data):
    '''
    
    This function allows to convert the list of dictionaries, containing the
    scraped info to be converted into an sql database stored locally
    Function has been adapted to process raw data, convert it into a pandas
    dataframe and then to sql database using sqlalchemy 

    Returns: 
        None
    '''
    data_to_list=[]
    for item in data:
        data_to_list.append([list(item.keys())[0], list(item.values())[0][1], list(item.values())[0][4] ])
    df = pd.DataFrame (data_to_list, columns = ['Link', 'Gender', 'Item'])
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    HOST = 'localhost'
    USER = 'postgres' 
    PASSWORD = '123456' 
    DATABASE = 'scraper' 
    PORT = 5432
    engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    
    df.to_sql('sql_dataset', engine, if_exists='replace')
    return

# ASSUMES INPUT DATA IS IN THIS FORM 
# data=[{'https://www2.hm.com/en_gb/productpage.1033298001.html': ['HM.com', 'Women', 'Jackets &amp; Coats', 'Coats', 'Coat']},
# {'https://www2.hm.com/en_gb/productpage.1033298001.html': ['HM.com', 'Women', 'Jackets &amp; Coats', 'Coats', 'Coat']}]







