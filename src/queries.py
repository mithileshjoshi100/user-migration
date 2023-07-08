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

'''
1. Add youe Queries in this file
2. Must query Id filed for each object (as its required for maping old to new)
3. You can add any non-lookup filed to existing query without changing code
4. all the filed present in the query will added to new record in new org except
    reletionship filed (name consist of '.' ) and Id filed. 
3. In {Keys} is will replace by In (usernames) at runtime
4. Make sure syntax of query is correct and user have permition to read and write all fileds 
'''

contact_query = '''
SELECT Id, FirstName, LastName, AccountId, MailingCountry, Department,Department__c , Functional_Role__c, Email 
FROM Contact 
WHERE Is_community_user__c = true and Email IN {keys}
'''

user_query= '''
SELECT Id,ContactId, email,Username, FirstName, LastName, GEHealthcare_CDX_Terms_and_Conditions__c,Department, Function_Role__c,Functional_Role__c,  GEHealthcare_CDX_Email_Phone_Consent__c,ProfileId,  TimeZoneSidKey, LanguageLocaleKey, LocaleSidKey, Alias, CommunityNickname, Country, EmailEncodingKey, IsActive, isValidated__c 
FROM User 
WHERE  Profile.name IN ('GEHC Logon Community User','GEIDP Logon Community User','GEIDP External Identity User') 
AND Email in {keys}
'''

permissionsetassignment_query = '''
SELECT Id, AssigneeId, PermissionSetId,Assignee.Email 
FROM PermissionSetAssignment 
WHERE Assignee.Profile.name IN ('GEHC Logon Community User','GEIDP Logon Community User','GEIDP External Identity User') 
AND Assignee.Email in {keys}          
'''

customerappaoleaccess_query = '''
SELECT Id, UserID__c,contact__r.email, Contact__c,ConnectedAppID__c,CSM_Admin__c, custAdmin__c,CSM_Admin_Role__c, AppRole__c, Name, isPrimary__c, isProgressive__c, isParallelApp__c 
FROM GEIDP_Customer_App_Role_Access__c 
WHERE User__r.Profile.name IN ('GEHC Logon Community User','GEIDP Logon Community User','GEIDP External Identity User') 
AND User__r.Username IN {keys}
'''

contactadditionalinformation_query = '''
SELECT Id, Contact__r.Email,Contact__c,  Facilities_List__c, Modalities_List__c, Assets_List__c, GEHC_Community_IB_Asset__c, GEHC_Onboarded__c, GEIDP_FacilitiesUpdated__c, GEIDP_MobileOnboarded__c, GEHC_MyOrdersOnboarding__c,AdminTnCCheck__c, Departments__c, PreferenceTypes__c 
FROM Contact_Additional_Information__c
WHERE Contact__r.Community_user__r.ContactId != null 
AND Contact__r.Email IN {keys}
'''

usersfrommanualregflow_query = '''
SELECT Id, Status__c, ApplicationCountry__c,ProgressiveApplicationName__c, System_ID__c, Profession__c,Sumtotal_Callout_Status__c,  ApplicationName__c,Serial_Number__c, OwnerId ,User__r.Email,User__c, Contact__r.Email,Contact__c, Account__c, isNewContact__c,  TnCCheck__c, NotificationType__c,Message__c, isGehcSiteRegistration__c,Rejection_Reason__c,  Organisation__c, Department__c ,isEcommerceRegistration__c, isGuestCheckout__c, b2bRegistration__c, UserRole__c,ThirdPartyEmployerName__c, isThirdPartyEmployee__c, CustomerAccountNumber__c, First_Name_Local__c, Last_Name_Local__c  
FROM GEIDPUsersFromManualRegFlow__c 
WHERE User__r.Email IN {keys}         
'''