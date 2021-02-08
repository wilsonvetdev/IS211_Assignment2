import argparse
import urllib.request
import logging
import ssl
import pprint
import csv, re
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context

LOG_FILENAME = 'error.log'
logging.basicConfig(
    filename = LOG_FILENAME,
    level = logging.ERROR,
    format = 'Error processing line %(lineno)d %(message)s'
)

def download_data(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = response.read()
        
        with open('csv_data.csv', 'w') as csv_file:
            data = data.decode('utf-8').splitlines()
            writer = csv.writer(csv_file, delimiter = '\t')
            for line in data:
            # writerow() needs a list of data to be written, so split at all empty spaces in the line 
                writer.writerow(re.split('\t', line))

# https://stackoverflow.com/questions/51089194/python-convert-bytes-unicode-tab-delimited-data-to-csv-file

def process_birthdate(birthdate):
    formatted_birthdate = datetime.strptime(birthdate, '%d/%m/%Y')
    return formatted_birthdate


def process_data(file_content):

    birthday_dict = {}

    with open(file_content, newline='') as csv_file:
        people_reader = csv.DictReader(csv_file, delimiter=',')
        for row in people_reader:
            try:
                birthdate = process_birthdate(row['birthday'])
                birthday_dict[row['id']] = (row['name'], birthdate)
            except ValueError:
                logging.error("for ID " + row['id'])
    
    return birthday_dict


# download_data('https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
# print(process_data('csv_data.csv'))

def displayPerson(id, personData):
    pass

def main(url):
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
