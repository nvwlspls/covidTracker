#!/usr/bin/env python3

import requests
import time
import os
from bs4 import BeautifulSoup
from twilio.rest import Client
from access.access import SPI, AUTH_TOKEN, PHONE_NUMBER

COVID_NUM = 0

account_sid = SPI
auth_token = AUTH_TOKEN
client = Client(account_sid, auth_token)
print(os.getcwd())
while True:

    site = requests.get('https://www.sandiegocounty.gov/content/sdc/hhsa/programs/phs/community_epidemiology/dc/2019-nCoV/status.html')
    soup = BeautifulSoup(site.content, 'html.parser')
    this_num = int(soup.select(".table > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > b:nth-child(1)")[0].text)

    if this_num != COVID_NUM:
        
        diff = this_num -  COVID_NUM
        COVID_NUM = this_num

        message = "San Diego has reported {} new Coronvavirus cases today.  The total is now {}".format(diff, this_num)

        message = client.messages \
                .create(
                     body=message,
                     from_='+12028901613',
                     to=PHONE_NUMBER
                 )
    
    time.sleep(60)