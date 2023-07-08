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


import logging

import src.lib as lib
from src.sf_connection import sf_new
sf = sf_new()


@lib.add_call_logs
def insert_contact():
    """
    insert contacts to org
    record new contact id to csv file
    provided by csv file
    """
    # read_contact file
    df_contact = lib.read_df('df_contact.csv')

    # replace nan(Empty Cell) with ''
    df_contact = df_contact.fillna('')
    # insert it to org
    for index, row in df_contact.iterrows():
        record = dict(
            filter(
                lambda k: '.' not in k[0] and k[0] != 'Id',
                row.to_dict().items())
            )
        logging.debug(f'creating Contact record for {row["Email"]}')
        inserted_c = sf.Contact.create(record)

        df_contact.at[index, 'new_Id'] = inserted_c['id']

    lib.export_df(df_contact, 'df_contact.csv')
    logging.info('Contact inserted :)')


@lib.add_call_logs
def insert_users():
    """
    insert users to org
    record new user id to csv file
    provided by csv file
    """

    # read the user file
    df_users = lib.read_df('df_users.csv')

    logging.debug("started  lookup for new contact for user records")
    # read contact file
    df_contact = lib.read_df('df_contact.csv')

    # lookup and update contact related to user
    for index, row in df_users.iterrows():
        contact_record = df_contact[df_contact['Id'] == row['ContactId']]
        new_contact_id = contact_record['new_Id'][0]
        df_users.at[index, 'ContactId'] = new_contact_id
    logging.debug("Lookup finished :)")

    # insert user one by one
    for index, row in df_users.iterrows():
        logging.debug(f'creating User record for {row["Email"]}')
        record = lib.filter_record(row)
        inserted_user = sf.User.create(record)
        df_users.at[index, 'new_Id'] = inserted_user['id']
    
    lib.export_df(df_users, 'df_users.csv')
    logging.info('Users inserted :)')


@lib.add_call_logs
def insert_psa():
    """PermissionSetAssignment
    """
    df_psa = lib.read_df('df_psa.csv')
    df_users = lib.read_df('df_users.csv')
    print(df_psa)
    # lookup and update contact related to user
    for index, row in df_psa.iterrows():
        user_record = df_users[df_users['Id'] == row['AssigneeId']]
        print(user_record)
        new_user_id = user_record['new_Id'][0]
        df_psa.at[index, 'AssigneeId'] = new_user_id
    logging.debug("Lookup finished :)")
    print(df_psa)
    # insert user one by one
    for index, row in df_psa.iterrows():
        
        record = lib.filter_record(row)
        try:
            inserted_psa = sf.PermissionSetAssignment.create(record)
            df_psa.at[index, 'new_Id'] = inserted_psa['id']
        except:
            df_psa.at[index, 'new_Id'] = '00000000000'
    lib.export_df(df_psa, 'df_psa.csv')

