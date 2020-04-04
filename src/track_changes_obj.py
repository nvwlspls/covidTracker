import os
import requests
import json
import datetime
from bs4 import BeautifulSoup

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

    def track_changes(self):
        
        # check for data files
        data_files_exist = self.check_for_data_files()


        # if check is false create the files 
        if not data_files_exist:
            self.create_default_data()
        
        # read data
        data_file  = os.pthat.join(self.data_dir, "covid_data.json")
        old_data = json.load("")
        # read the etag data from the files
        
        # get the curr etag from the site
        
        # if new etag != old etag
            # get the old case num
            # get the old death num

            # get the curr case num
            # get the curr death num

            # new cases = curr case num - old case num
            # new deaths = curr death num - old death num

            # save data to file
            # close file

            # compose message

            # send message

            #

        # else:
            # pass
        pass
    
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

        curr_data_dict["ETag"] = curr_etag
        
        # create dict for file
        output_dict = {}
        output_dict[timestamp] = curr_data_dict

        # open files
        f = open(os.path.join(self.data_dir, "covid_data.json"), "w+")
        
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

"""
example data structure
{
    2020-03-31: {'cases':1
                    'deaths':2,
                    'etag': 'absdfd'}
}
"""