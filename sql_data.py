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
    for key, item in data.items():
        
        data_to_list.append([key, item['Product Type'][0], item['Product'], item['Product Type'][1], item['Product Type'][2],
                            item['Price'], item['Length'], item['Composition'], item['Care instructions'], item['Description'], 
                            item['URL'], item['SRC']])

    cols = ['ID', 'Gender', 'Item', 'Item Type', 'Item Sub-type', 'Price', 'Length', 'Composition', 'Care instructions', 'Description', 
            'URL', 'SRC'] 
    df = pd.DataFrame (data_to_list, columns = cols)   
    print(df)
    # DATABASE_TYPE = 'postgresql'
    # DBAPI = 'psycopg2'
    # HOST = 'localhost'
    # USER = 'postgres' 
    # PASSWORD = '123456' 
    # DATABASE = 'scraper' 
    # PORT = 5432

    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    ENDPOINT = 'scraper-database.ccrswyrqul7x.eu-west-2.rds.amazonaws.com'
    USER = 'postgres'
    PASSWORD = 'Barney321'
    PORT = 5432
    DATABASE = 'postgres'
    engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
    
    df.to_sql('sql_dataset', engine, if_exists='replace')
    return None







