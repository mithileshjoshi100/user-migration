### -ACCENTURE CONFIDENTIAL-
### Type: Source Code
###
### Copyright (c) 2023, ACCENTURE
### All Rights Reserved.
###
### This unpublished material is proprietary to ACCENTURE. The methods and
### techniques described herein are considered trade secrets and/or
### confidential. Reproduction or distribution, in whole or in part, is
### forbidden except by express written permission of ACCENTURE.


import pandas as pd
import numpy as np
import logging
from simple_salesforce import format_soql


def add_call_logs(func):
    """
    decorator function to
    log the name,start-time and end-time of exicution

    Args:
        func (function): function to exicute
    """
    def wraper(*args, **kwargs):
        logging.debug(f'calling function{func.__name__}')
        result = func(*args, **kwargs)
        logging.debug(f'function call ends {func.__name__}')
        return result
    
    return wraper


@add_call_logs
def sf_api_query(data):
    """
    convert the api responce to pandas DataFream

    Args:
        data (dict): responce of query from simple_salesforce

    Returns:
        DataFream: Table of query result
    """
    
    if data['totalSize'] == 0: 
        print('No Records found')
        return None
    df = pd.DataFrame(data['records']).drop('attributes', axis=1)
    
    listColumns = list(df.columns)
    for col in listColumns:
        if any (isinstance (df[col].values[i], dict) 
                for i in range(0, len(df[col].values))):
            df = pd.concat(
                [
                df.drop(columns=[col]),
                df[col].apply(pd.Series)
                .drop('attributes',axis=1).add_prefix(col+'.')
                ],
                 axis=1)
            new_columns = np.setdiff1d(df.columns, listColumns)
            for i in new_columns:
                listColumns.append(i)
    return df


@add_call_logs
def export_df(df,name):
    """
    validate and export datafream to csv file with given name

    Args:
        df (DataFream): DataFream to be exported
        name (str): name for the file to export
    """
    if df is None :
        logging.error(f'Detafream is emplty can not store to file {name}')
        return
    logging.debug(f'writing to file/{name}')
    df.to_csv(f'files/{name}',index=False)



@add_call_logs
def read_df(name):
    """
    read the file
    handle exceptions
    return empty DataFrame if file not found

    Args:
        name (str):  name of file to read

    Returns:
        DataFrame: Tabel from csv file
    """
    logging.debug(f'reading file files/{name}')
    
    try:
        df = pd.read_csv(f'files/{name}')
    except FileNotFoundError as e:
        logging.warning(f'file {name} not found,'
                        +' probably their is no records to insert')
        df = pd.DataFrame()
    return df


@add_call_logs
def soql_query_call(sf,query,keys):
    """
    format and call the soql query
    handle exceptions
    provide logs

    Args:
        sf (Object): instance if salesforce org
        query (string): raw soql query
        keys (set of strings): set of emails

    Returns:
        json type responce: responce of soql query
    """
    formated_query = format_soql(
            query = query,
            keys = list(keys)
        )
    logging.debug('query'+formated_query)
    r=sf.query_all(
        formated_query
    )
    logging.debug('query exicution sucess')
    return r

    
def filter_record(row):
    """
    filter out the row 
    remove reletionship fileds and Id filed

    Args:
        row (Pandas Series): single row of datafream

    Returns:
        dict: pure record to insert to salesforce object
    """
    record = dict(
            filter(
            lambda k: '.' not in k[0] and k[0] != 'Id',
            row.to_dict().items())
            )

    return record