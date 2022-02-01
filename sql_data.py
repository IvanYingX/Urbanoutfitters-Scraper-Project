from sqlalchemy import create_engine
import pandas as pd
import json

def sql_data(data):
    '''
    
    This function allows to convert the list of dictionaries, containing the
    scraped info to be converted into an sql database stored locally
    Function has been adapted to process raw data, convert it into a pandas
    dataframe and then to sql database using sqlalchemy 

    Returns: 
        None
    '''
    # data_to_list=[]
    # for key, item in data.items():
        
    #     data_to_list.append([key, item['Product Type'][0], item['Product'], item['Product Type'][1], item['Product Type'][2],
    #                         item['Price'], item['Length'], item['Composition'], item['Care instructions'], item['Description'], 
    #                         item['URL'], item['SRC']])

    # cols = ['ID', 'Gender', 'Item', 'Item Type', 'Item Sub-type', 'Price', 'Length', 'Composition', 'Care instructions', 'Description', 
    #         'URL', 'SRC']

    # df = pd.DataFrame (data_to_list, columns = cols)
    cols_tmp = []
    for item in data.items():
        for key in item[1].keys():
            cols_tmp.append(key)
        
    
    cols_tmp = list(set(cols_tmp))
    cols_tmp.remove('Art. No.')
    cols_tmp.remove('Product Type')
    cols_tmp.remove('Product')
    cols_tmp.remove('Price')
    cols_tmp.remove('URL')
    cols_tmp.remove('SRC')
    cols_tmp.sort()
    cols = ['ID', 'Gender', 'Item', 'Item Type', 'Item Sub-type', 'Price']
    for x in cols_tmp:
        cols.append(x)
    cols.append('URL')
    cols.append('SRC')
    print(cols)

    data_to_list=[]
    for key, item in data.items():
        list_tmp = []
        for col in cols:
            if col == 'ID':
                list_tmp.append(key)
            elif col == 'Gender':
                list_tmp.append(item['Product Type'][0])
            elif col == 'Item':
                list_tmp.append(item['Product'])
            elif col == 'Item Type':
                list_tmp.append(item['Product Type'][1])
            elif col == 'Item Sub-type':
                list_tmp.append(item['Product Type'][2])
            elif col == 'Price':
                list_tmp.append(item['Price'])
            elif col == 'URL':
                list_tmp.append(item['URL'])
            elif col == 'SRC':
                list_tmp.append(item['SRC'])
            else:
                if col in item:
                    list_tmp.append(item[col])
                else:
                    list_tmp.append(None)

        data_to_list.append(list_tmp)
    

    #print(data_to_list)
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


# if __name__ == '__main__':
#     with open('female_page_dict.json') as json_file:
#         female_dict = json.load(json_file)

#     with open('male_page_dict.json') as json_file:
#         male_dict = json.load(json_file)

#     female_dict.update(male_dict)
#     sql_data(female_dict)





