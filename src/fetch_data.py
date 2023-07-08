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
import src.usernames as usernames
import src.queries as queries

from src.sf_connection import sf_old
sf = sf_old()


@lib.add_call_logs
def fetch_contacts():
    """
    fetch the contact from old org
    provided by email set
    """

    r = lib.soql_query_call(
        sf=sf,
        query=queries.contact_query,
        keys=usernames.emails
    )
    df_contact = lib.sf_api_query(r)

    lib.export_df(df_contact, 'df_contact.csv')
    logging.info('Contacts Exported')
    

@lib.add_call_logs
def fetch_users():
    """
    fetch the users from org
    provided by email set
    """
    r = lib.soql_query_call(
        sf=sf,
        query=queries.user_query,
        keys=usernames.emails
    )
    df_users = lib.sf_api_query(r)
    
    lib.export_df(df_users, 'df_users.csv')
    logging.info('Users Exported')


@lib.add_call_logs
def fetch_psa():
    """
    fetch the PermissionSetAssignment from org
    provided by email set
    """
    r = lib.soql_query_call(
        sf= sf,
        query= queries.permissionsetassignment_query,
        keys= usernames.emails
    )
    df_psa = lib.sf_api_query(r)

    lib.export_df(df_psa,'df_psa.csv')

        
@lib.add_call_logs
def fetch_approllaccess():
    """
    fetch the GEIDP_Customer_App_Role_Access__c from org
    provided by email set
    """
    r = lib.soql_query_call(
        sf= sf,
        query= queries.customerappaoleaccess_query,
        keys= usernames.emails
    )
    df_approllaccess = lib.sf_api_query(r)

    lib.export_df(df_approllaccess,'df_approllaccess.csv')
    logging.info('GEIDP_Customer_App_Role_Access__c Exported')
    
# not tested yet
@lib.add_call_logs
def fetch_contact_additional_information():
    """
    fetch Contact_Additional_Information__c records from org
    provided by email set
    """
    r = lib.soql_query_call(
        sf= sf,
        query= queries.contactadditionalinformation_query,
        keys= usernames.emails
    )
    df_cai = lib.sf_api_query(r)

    lib.export_df(df_cai,'df_cai.csv')
    logging.info('Contact_Additional_Information__c Exported')


# @lib.add_call_logs
# def fetch_umr():
#     """
#     fetch GEIDPUsersFromManualRegFlow__c records from org
#     provided by email set
#     """
#     r = lib.soql_query_call(
#         sf= sf,
#         query= queries.usersfrommanualregflow_query,
#         keys= usernames.emails
#     )
#     df_umr = lib.sf_api_query(r)

#     lib.export_df(df_umr,'df_umr.csv')
#     logging.info('GEIDPUsersFromManualRegFlow__c Exported')
