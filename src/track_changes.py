import requests
import time
import os
import json
from json.decoder import JSONDecodeError
from bs4 import BeautifulSoup
from twilio.rest import Client
from access.access import SPI, AUTH_TOKEN, PHONE_NUMBER

# access infor
account_sid = SPI
auth_token = AUTH_TOKEN

# create client
client = Client(account_sid, auth_token)

# requests
target_url = 'https://www.sandiegocounty.gov/content/sdc/hhsa/programs/phs/community_epidemiology/dc/2019-nCoV/status.html'


# get the data from the last change
change_data_file = open(os.path.join(os.getcwd(), 'data', 'change_info.json'), 'w+')

import pdb; pdb.set_trace();

try:
    change_data = json.load(change_data_file)
except JSONDecodeError:
    change_data = {}
    # get the etag value and remove the quotes
    change_data['etag'] = requests.head(target_url).headers['ETag'].strip('\"')
    json.dump(change_data, change_data_file)
    change_data_file.close()

# if the etag is the same then we can stop

curr_etag = requests.head(target_url).headers['ETag'].strip('\"')

if curr_etag != change_data:
    # 
    site = requests.get(target_url)
    soup = BeautifulSoup(site.content, 'html.parser')
    case_num = int(soup.select(".table > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > b:nth-child(1)")[0].text)
    death_num = int(soup.select(".table > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(21) > td:nth-child(2)").text)

    #open this file
    case_data_file = open(os.path.join(os.getcwd()), 'data', 'case_data.json', \
    'w+' )

    try:
        case_data = json.load(case_data_file)
    except JSONDecodeError:
        case_data = {}
        case_data['total_cases'] = case_num
        


# data dir
data_dir = os.path.join(os.getcwd(), 'data')

stats_data = open(os.path.join(data_dir, 'stats'), 'w+')

# current numbers

diff = case_num -  COVID_NUM
COVID_NUM = case_num

text = "San Diego has reported {} new Coronvavirus cases today.  The total is now {}".format(diff, this_num)

message = client.messages \
        .create(
                body=text,
                from_='+12028901613',
                to=PHONE_NUMBER
            )
