from sqlalchemy import create_engine
import pandas as pd
import json

def sql_data(data, database_dict):
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
    cols_custom = []
    for item in data.items():
        for key in item[1].keys():
            cols_custom.append(key)
        
    
    cols_custom = list(set(cols_custom))
    cols_custom.remove('Art. No.')
    cols_custom.remove('Product Type')
    cols_custom.remove('Product')
    cols_custom.remove('Price')
    cols_custom.remove('URL')
    cols_custom.remove('SRC')
    cols_custom.sort()
    cols_generic = ['ID', 'Gender', 'Item', 'Item Type', 'Item Sub-type', 'Price', 'URL', 'SRC']
    cols = cols_generic + cols_custom
    cols_custom1 = ['ID'] + cols_custom
    
    #print(cols_custom)
    

    data_generic_to_list=[]
    data_custom_to_list=[]
    gender = ''
    for key, item in data.items():
        
        list_generic_tmp, list_custom_tmp, gender = unpack_data_from_dict(cols, item, key, gender)

        data_generic_to_list.append(list_generic_tmp)
        data_custom_to_list.append(list_custom_tmp)
    

    #print(data_to_list)
    df_generic = pd.DataFrame (data_generic_to_list, columns = cols_generic)
    df_custom = pd.DataFrame (data_custom_to_list, columns = cols_custom1)
     
    DATABASE_TYPE, DBAPI, ENDPOINT, USER, PASSWORD, PORT, DATABASE = unpack_rds_params(database_dict)

    engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
    
    df_generic.to_sql('base_info', engine, if_exists='replace')
    df_custom.to_sql('custom_info', engine, if_exists='replace')
    return None

def unpack_rds_params(params_dict):
    return (params_dict['DATABASE_TYPE'], params_dict['DBAPI'], params_dict['ENDPOINT'],
                params_dict['USER'], params_dict['PASSWORD'], params_dict['PORT'], params_dict['DATABASE'])

def unpack_data_from_dict(cols, item, key, gender):
    
    list_generic_tmp = []
    list_custom_tmp = []
    for col in cols:
        if col == 'ID':
            list_generic_tmp.append(key)
            list_custom_tmp.append(key)
        elif col == 'Gender':
            if item['Product Type'][0] == 'Men' or item['Product Type'][0] == 'Women':
                list_generic_tmp.append(item['Product Type'][0])
                gender = item['Product Type'][0]
            else:
                list_generic_tmp.append(gender)
        elif col == 'Item':
            list_generic_tmp.append(item['Product'])
        elif col == 'Item Type':
            if len(item['Product Type']) > 1:
                list_generic_tmp.append(item['Product Type'][1])
            else:
                list_generic_tmp.append(None)
        elif col == 'Item Sub-type':
            if len(item['Product Type']) > 2:
                list_generic_tmp.append(item['Product Type'][2])
            else:
                list_generic_tmp.append(None)
        elif col == 'Price':
            list_generic_tmp.append(item['Price'])
        elif col == 'URL':
            list_generic_tmp.append(item['URL'])
        elif col == 'SRC':
            list_generic_tmp.append(item['SRC'])
        else:
            if col in item:
                list_custom_tmp.append(item[col])
            else:
                list_custom_tmp.append(None)
    
    return list_generic_tmp, list_custom_tmp, gender
    

if __name__ == '__main__':
    with open('female_page_dict.json') as json_file:
        female_dict = json.load(json_file)

    with open('male_page_dict.json') as json_file:
        male_dict = json.load(json_file)

    with open('data_storage_credentials.json') as json_file:
        storage_details = json.load(json_file)
        rds_details = storage_details['rds']

    female_dict.update(male_dict)
    sql_data(female_dict, rds_details)





