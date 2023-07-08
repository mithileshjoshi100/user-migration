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


from simple_salesforce import Salesforce
import json
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename='basiclog.log'
)


try:
    f = open('src/creds.json')
    creds = json.load(f)
except FileNotFoundError:
    logging.error("src/creds.json file not found :(")
    logging.error("please create file and provide your creds")
    exit(1)
    assert FileNotFoundError
except json.decoder.JSONDecodeError:
    logging.error("JSON Format error :(, please correct the format")
    exit(1)


def sf_new():
    sf_new_instence = Salesforce(
        username=creds["new_org"]["username"],
        password=creds["new_org"]["password"],
        domain='test',
        consumer_key=creds["new_org"]["consumer_key"],
        consumer_secret=creds["new_org"]["consumer_secret"]
        )
    return sf_new_instence


def sf_old():
    sf_new_instence = Salesforce(
        username=creds["old_org"]["username"],
        password=creds["old_org"]["password"],
        domain='test',
        consumer_key=creds["old_org"]["consumer_key"],
        consumer_secret=creds["old_org"]["consumer_secret"]
        )
    return sf_new_instence
