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
    log the name,start-time and end-time of execution

    Args:
        func (function): function to execute
    """

    def wrapper(*args, **kwargs):
        logging.debug(f'calling function{func.__name__}')
        result = func(*args, **kwargs)
        logging.debug(f'function call ends {func.__name__}')
        return result

    return wrapper


@add_call_logs
def sf_api_query(data):
    """
    convert the api response to pandas DataFrame

    Args:
        data (dict): response of query from simple_salesforce

    Returns:
        DataFrame: Table of query result
    """

    if data['totalSize'] == 0:
        print('No Records found')
        return None
    df = pd.DataFrame(data['records']).drop('attributes', axis=1)

    list_columns = list(df.columns)
    for col in list_columns:
        if any(isinstance(df[col].values[i], dict)
               for i in range(0, len(df[col].values))):
            df = pd.concat(
                [
                    df.drop(columns=[col]),
                    df[col].apply(pd.Series)
                    .drop('attributes', axis=1).add_prefix(col + '.')
                ],
                axis=1)
            new_columns = np.setdiff1d(df.columns, list_columns)
            for i in new_columns:
                list_columns.append(i)
    return df


@add_call_logs
def export_df(df, name):
    """
    validate and export dataframe to csv file with given name

    Args:
        df (DataFrame): DataFrame to be exported
        name (str): name for the file to export
    """
    if df is None:
        logging.error(f'Dataframe is empty can not store to file {name}')
        return
    logging.debug(f'writing to file/{name}')
    df.to_csv(f'files/{name}', index=False)


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
                        + ' probably their is no records to insert')
        logging.error(e)
        df = pd.DataFrame()
    
    df = df.fillna('')
    return df


@add_call_logs
def soql_query_call(sf, query, keys):
    """
    format and call the soql query
    handle exceptions
    provide logs

    Args:
        sf (Object): instance if salesforce org
        query (string): raw soql query
        keys (set of strings): set of emails

    Returns:
        json type response: response of soql query
    """
    formatted_query: str = format_soql(
        query=query,
        keys=list(keys)
    )
    logging.debug('query' + formatted_query)
    r = sf.query_all(
        formatted_query
    )
    logging.debug('query exicution success')
    return r


def filter_record(row):
    """
    filter out the row 
    remove relationship filed and ID filed

    Args:
        row (Pandas Series): single row of dataframe

    Returns:
        dict: pure record to insert to salesforce object
    """
    record = dict(
        filter(
            lambda k: 
                '.' not in k[0] 
                and k[0] != 'Id' 
                and k[0] != 'new_Id',
            row.to_dict().items())
    )

    return record


def v_lookup_id(
        df_current,
        df_lookup,
        current_record_id,
    ):
    for index, row in df_current.iterrows():
        contact_record = df_lookup[df_lookup['Id'] == row[current_record_id]]
        new_contact_id = contact_record['new_Id'][0]
        df_current.at[index, current_record_id] = new_contact_id  
    
    return df_current