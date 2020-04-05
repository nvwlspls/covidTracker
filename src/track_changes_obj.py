import os
import requests
import json
import datetime
from bs4 import BeautifulSoup
from twilio.rest import Client
from access.access import SPI, AUTH_TOKEN, TEST_NUMBERS


class TrackCovidChanges():
    """
    An object that can track the changes on a page
    """

    def __init__(self):
        super().__init__()
        self.url = \
        'https://www.sandiegocounty.gov/content/sdc/hhsa/programs/phs/' + \
        'community_epidemiology/dc/2019-nCoV/status.html'
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.data_file = os.path.join(self.data_dir, 'covid_data.json')

    def track_changes(self):

        # check for data files
        data_files_exist = self.check_for_data_files()


        # if check is false create the files 
        if not data_files_exist:
            self.create_default_data()

        # read data
        import pdb; pdb.set_trace();
        data_file  = open(self.data_file, 'r')
        old_data = json.load(data_file)
        data_file.close()

        # get max data to get latest data result
        latest_date = self.get_max_date(old_data)
                
        # if new etag != old etag
        if old_data[latest_date]['etag'] != self.get_curr_etag_header():
            
            current_timestamp = self.create_key_timestamp()
            current_data = self.get_curr_data()

            # get the old case num
            old_case_num = old_data[latest_date]['case_num']
            # get the old death num
            old_death_num = old_data[latest_date]['death_num']

            # get the curr case num
            curr_case_num = current_data['case_num']
            # get the curr death num
            curr_death_num = current_data['death_num']

            # new cases / deaths
            new_cases = curr_case_num - old_case_num
            new_deaths = curr_death_num - old_death_num

            # save data to file
            old_data[current_timestamp] = current_data
            
            data_file = open(self.data_file, 'w+')
            json.dumps(old_data, data_file)
            
            # close file
            data_file.close()

            # compose message
            message_text = "San Diego County reported {} new cases f COVID19" +\
                " and {} new deaths. Source: https://bit.ly/2V0Havj"
            # send message

        # else:
            # pass
        pass
    
        def send_text_message(self, text, numbers):
            """
            Send text message 
            """

            client = Client(SPI, AUTH_TOKEN)
            # send message
            for number in TEST_NUMBERS:

                message = client.messages \
                        .create(
                                body=text,
                                from_='+12028901613',
                                to=number
                            )


    def get_max_date(self, data_dict):
        """
        get the max date from the data keys
        """
        
        return max(list(data_dict.keys()))
        
    def create_key_timestamp(self):
        """
        create a timestamp that will be used for the key
        example "2020-03-30-1600"
        """
        
        return datetime.datetime.now().strftime("%Y-%m-%d-%H%M")


    def get_curr_etag_header(self):
        """
        get the current etag header
        """

        return requests.head(self.url).headers['Etag']


    def check_for_data_files(self):
        """
        Check the data dir for default files
        """
        
        data_dir_files = os.listdir(self.data_dir)
        
        if "covid_data.json" not in data_dir_files:
            return False
        
        return True


    def load_data(self):
        """
        load the current data
        """
        pass

    def create_default_data(self):
        
        """
        Create the default files and populate them with generic data
        """

        # get current data
        curr_data_dict = self.get_curr_data()
        curr_etag = self.get_curr_etag_header()
        timestamp = self.create_key_timestamp()

        curr_data_dict["etag"] = curr_etag
        
        # create dict for file
        output_dict = {}
        output_dict[timestamp] = curr_data_dict

        # open files
        f = open(self.data_file, "w+")
        
        # write current data to file
        json.dump(output_dict, f)

        # close files
        f.close()
        
        return output_dict
        
    def get_curr_data(self):
        
        curr_page = requests.get(self.url)
        soup = BeautifulSoup(curr_page.content, 'html.parser')

        case_num = int(soup.select(".table > table:nth-child(1) > " +
        "tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > " +
         "b:nth-child(1)")[0].text.replace(",", ""))
        
        death_num = int(soup.select(".table > table:nth-child(1) >" + \
            " tbody:nth-child(1) > tr:nth-child(21) > td:nth-child(2)")[0].text)
        
        # create data dict
        data_dict = {}
        data_dict["case_num"] = case_num
        data_dict["death_num"] = death_num
        
        return data_dict


apples = TrackCovidChanges()

apples.track_changes()

"""
example data structure
{
    2020-03-31: {'cases':1
                    'deaths':2,
                    'etag': 'absdfd'}
}
"""