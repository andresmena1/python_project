# import all needed modules
from curses.ascii import isdigit
import os
from os import path
import datetime
from datetime import timedelta
import re
from statistics import mode
import string
import requests
import collections

#url of file log
file_url = 'https://s3.amazonaws.com/tcmg476/http_access_log'

#check to see if file exists
file_exists = (os.path.exists("server_log.txt"))
print ("File exists: " + str(file_exists))

#download file if it does not exist
if file_exists == False:
    download_file = requests.get(file_url, allow_redirects=True)
    open('server_log.txt', 'wb').write(download_file.content)

#open the file
fh = open('server_log.txt')

#variable for number of lines in file
number_lines = fh.readlines()

#print how many total lines there are in the file
print('There are a total of ' + str(len(number_lines)) + ' server requests in the file\n')

#regex expression
regex = re.compile('(.*?) - - \[(.*?):(.*) .*] \"[A-Z]{3,6} (.*?) HTTP.*\" (\d{3}) (.*)')

#counter for last six months
counter = 0

#days dictionary
days = {
     1: 0,
     2: 0,
     3: 0,
     4: 0,
     5: 0,
     6: 0,
     7: 0,
     8: 0,
     9: 0,
     10: 0,
     11: 0,
     12: 0,
     13: 0,
     14: 0,
     15: 0,
     16: 0,
     17: 0,
     18: 0,
     19: 0,
     20: 0,
     21: 0,
     22: 0,
     23: 0,
     24: 0,
     25: 0,
     26: 0,
     27: 0,
     28: 0,
     29: 0,
     30: 0,
     31: 0,
}
#months dictionary
months = {
     1: 0,
     2: 0,
     3: 0,
     4: 0,
     5: 0,
     6: 0,
     7: 0,
     8: 0,
     9: 0,
     10: 0,
     11: 0,
     12: 0,
}

#weekday dictionary
day_of_week = {
     0: 0,
     1: 0,
     2: 0,
     3: 0,
     4: 0,
     5: 0,
     6: 0,
}

#list for last six months of entries
time_list = []
file_list = []
code_list = []
#loop that splits log file and appends to time list
for lines in number_lines:
     split_log = regex.split(lines)
     try:
          date_stamp = datetime.datetime.strptime(split_log[2], '%d/%b/%Y')
          time_list.append(date_stamp)
          months[date_stamp.month] +=1
          days[date_stamp.day] +=1
          day_of_week[date_stamp.weekday()] +=1
          file_stamp = split_log[4]
          file_list.append(file_stamp)
          code_stamp = split_log[5]
          code_list.append(int(code_stamp))
     except:
          pass

#latest date in list and entry six months ago
latest_date = max(time_list)
six_month_ago = latest_date - timedelta(days=180)

#for loop that add to conuter number of entries in six month range
for i in time_list:
     if i > six_month_ago:
          counter +=1

#print number of request in last six months
print("There are a total of " + str(counter) + " requests in the last six months\n")

#print months dictionary
print("Number of requests per month: (January = 1)")
print(months)

#print weekday dictionary
print("\nNumber of requests made per day of the week: (Monday = 0)")
print(day_of_week)

#use mode to get most common file
most_common_file = mode(file_list)
print("\nThe most common file requested was: " + str(most_common_file))

#use collections to find least common file
least_common_file = collections.Counter(file_list).most_common()[-1]
print("\nThe least common requested file was: " + str(least_common_file))

#counters for error codes
code3counter = 0
code4counter = 0


#for loop to add to error counters
for i in code_list:
     if i in range(300,399):
          code3counter +=1
     elif i in range(400,499):
          code4counter +=1

#print number of each error type
print("\nThere are " + str(code3counter) + (" 300 error codes"))
print("\nThere are " + str(code4counter) + (" 400 error codes"))
