import argparse
import urllib.request
import logging
import datetime
import ssl
import pprint
import csv, re

ssl._create_default_https_context = ssl._create_unverified_context

def downloadData(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = response.read()
        
        with open('csv_data.csv', 'w') as csv_file:
            data = data.decode('utf-8').splitlines()
            writer = csv.writer(csv_file, delimiter = '\t')
            for line in data:
            # writerow() needs a list of data to be written, so split at all empty spaces in the line 
                writer.writerow(re.split("\t", line))

# https://stackoverflow.com/questions/51089194/python-convert-bytes-unicode-tab-delimited-data-to-csv-file

def processData(file_content):

    with open(file_content, newline='') as csv_file:
        people_reader = csv.DictReader(csv_file, delimiter=',')
        for row in people_reader:
            print(row)
        

    # fields = data.pop(0).split(',')

    # with open(file_content, 'w') as csv_file:
    #         csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
    #         csv_writer.writeheader()
        
    #         for i in range(len(data)):
    #             item = data[i].split(',')
    #             print({item[0]: (item[1], item[2])})
    


downloadData('https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
processData('csv_data.csv')

def displayPerson(id, personData):
    pass

def main(url):
    print(f"Running main with URL = {url}...")


# if __name__ == "__main__":
#     """Main entry point"""
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
#     args = parser.parse_args()
#     main(args.url)
