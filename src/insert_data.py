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
        record = lib.filter_record(row)
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

    df_psa = lib.v_lookup_id(
        df_current=df_psa,
        df_lookup=df_users,
        current_record_id='AssigneeId'
        ) 
    
    logging.debug("Lookup finished :)")
    print(df_psa)
    # insert user one by one
    for index, row in df_psa.iterrows():
        
        record = lib.filter_record(row)
        try:
            inserted_psa = sf.PermissionSetAssignment.create(record)
            df_psa.at[index, 'new_Id'] = inserted_psa['id']
        except:
            df_psa.at[index, 'new_Id'] = 'Not Inserted by Python Script'
    lib.export_df(df_psa, 'df_psa.csv')


@lib.add_call_logs
def insert_approllaccess():
    """GEIDP_Customer_App_Role_Access__c
    """

    # read files
    df_users = lib.read_df('df_users.csv')
    df_contact = lib.read_df('df_contact.csv')
    df_approllaccess = lib.read_df('df_approllaccess.csv')

    df_approllaccess = lib.v_lookup_id(
        df_current=df_approllaccess,
        df_lookup=df_users,
        current_record_id='UserID__c'
        ) 
     
    df_approllaccess = lib.v_lookup_id(
        df_current=df_approllaccess,
        df_lookup=df_contact,
        current_record_id='Contact__c'
        )   
    
    # insert GEIDP_Customer_App_Role_Access__c one by one
    for index, row in df_approllaccess.iterrows():
        
        record = lib.filter_record(row)
        try:
            inserted_ara = sf.GEIDP_Customer_App_Role_Access__c.create(record)
            df_approllaccess.at[index, 'new_Id'] = inserted_ara['id']
        except:
            df_approllaccess.at[index, 'new_Id'] = '########'
    
    lib.export_df(df_approllaccess, 'df_approllaccess.csv')

# not tested yet
@lib.add_call_logs   
def insert_contact_additional_information():
    """Contact_Additional_Information__c
    """

    df_contact = lib.read_df('df_contact.csv')
    df_cai = lib.read_df('df_cai.csv')

    df_cai = lib.v_lookup_id(
        df_current=df_cai,
        df_lookup=df_contact,
        current_record_id='Contact__c'
        )    

    # insert GEIDP_Customer_App_Role_Access__c one by one
    for index, row in df_cai.iterrows():
        
        record = lib.filter_record(row)
        try:
            inserted_cai = sf.Contact_Additional_Information__c.create(record)
            df_cai.at[index, 'new_Id'] = inserted_cai['id']
        except:
            df_cai.at[index, 'new_Id'] = '########'
    
    lib.export_df(df_cai, 'df_cai.csv')


def insert_umr():
    """GEIDPUsersFromManualRegFlow__c
    """

    df_users = lib.read_df('df_users.csv')
    df_contact = lib.read_df('df_contact.csv')
    df_umr = lib.read_df('df_umr.csv')

    df_umr = lib.v_lookup_id(
        df_current=df_umr,
        df_lookup=df_users,
        current_record_id='User__c'
        )  

    df_umr = lib.v_lookup_id(
        df_current=df_umr,
        df_lookup=df_contact,
        current_record_id='Contact__c'
        )  
 
    # insert GEIDPUsersFromManualRegFlow__c one by one
    for index, row in df_umr.iterrows():
        record = lib.filter_record(row)
        try:
            inserted_umr = sf.GEIDPUsersFromManualRegFlow__c.create(record)
            df_umr.at[index, 'new_Id'] = inserted_umr['id']
        except:
            df_umr.at[index, 'new_Id'] = '########'
    
    lib.export_df(df_umr, 'df_umr.csv')

# not tested
@lib.add_call_logs
def insert_geidp_entitled_feature():
    """GEIDP_Entitled_Feature__c
    """
    
    df_users = lib.read_df('df_users.csv')
    df_contact = lib.read_df('df_contact.csv')
    df_approllaccess = lib.read_df('df_approllaccess.csv')
    df_feature = lib.read_df('df_feature.csv')

    df_feature = lib.v_lookup_id(
        df_current=df_feature,
        df_lookup=df_users,
        current_record_id='User__c'
        )

    df_feature = lib.v_lookup_id(
        df_current=df_feature,
        df_lookup=df_contact,
        current_record_id='Contact__c'
        )  

    df_feature = lib.v_lookup_id(
        df_current=df_feature,
        df_lookup=df_approllaccess,
        current_record_id='GEIDP_Customer_App_Role_Access__c'
        )
    
    # insert GEIDP_Entitled_Feature__c one by one
    for index, row in df_feature.iterrows():
        record = lib.filter_record(row)
        try:
            inserted_record = sf.GEIDP_Entitled_Feature__c.create(record)
            df_feature.at[index, 'new_Id'] = inserted_record['id']
        except:
            df_feature.at[index, 'new_Id'] = '########'
    
    lib.export_df(df_feature, 'df_feature.csv')


    
    

    

