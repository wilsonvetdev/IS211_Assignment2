import argparse
import urllib.request
import logging
import ssl
import csv, re
import sys
from datetime import datetime

# url = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'

ssl._create_default_https_context = ssl._create_unverified_context

LOG_FILENAME = 'error.log'
logging.basicConfig(
    filename = LOG_FILENAME,
    level = logging.ERROR,
)

def prRed(skk): print("\033[91m{}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m{}\033[00m" .format(skk)) 

# https://www.geeksforgeeks.org/print-colors-python-terminal/

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
    formatted_birthdate = datetime.strptime(birthdate, '%d/%m/%Y').date()
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
                logging.error(f"Error processing line {int(row['id']) - 1} ID {row['id']}")
    
    return birthday_dict


def display_person(id):
    birthday_dict = process_data('csv_data.csv')
    return f"Person #{id} is {birthday_dict[id][0]} with a birthday of {birthday_dict[id][1]}."


def main(url):
    print("                                  ")
    print(f"Running main with URL = {url}...")
    print("                                  ")
    user_input = 0
    prYellow('Enter an ID from 1 - 100: ')
    user_input = input()

    while user_input: 
        try:
            if int(user_input) <= 0:
                print("                                  ")
                prRed('***** Exiting Program  *****')
                sys.exit()
            print("                                  ")
            prGreen(displayPerson(str(user_input)))
            main(url)

        except KeyError:
            prRed('***** No user found with that ID. *****')
            main(url)

        except ValueError:
            print("                                  ")
            prRed('***** Only integers allowed. *****')
            main(url)

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    download_data(args.url)
    main(args.url)
