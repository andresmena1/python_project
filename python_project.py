from pickle import TRUE
import os.path
import requests
import re
import datetime
from datetime import timedelta

#asks the user to enter their username for their system
user_name = str(input("What is your username?: "))

#defines variable for the file path of server log
# right now I have only got it to work in Windows, I will try to get it to run in Linux
server_log = 'C:\\Users\\' + user_name + '\\Downloads\\server.log'

#check if file exists already
file_exists = os.path.exists('C:\\Users\\' + user_name + '\\Downloads\\server.log')

#variable for number of lines
counter = 0

#if the file exists print total lines, if not it downloads the file then prints total lines
if file_exists == True:
    print ("File is already downloaded")
    fh = open(server_log)
    lines = fh.readlines()
    print("There are " + str(len(lines)) + " total lines in the server log.")
elif file_exists == False:
    url = 'https://s3.amazonaws.com/tcmg476/http_access_log'
    r = requests.get(url, allow_redirects=True)
    open('server.log', 'wb').write(r.content)
    print("File has been downloaded")
    fh = open(server_log)
    lines = fh.readlines()
    print("There are " + str(len(lines)) + " total lines in the server log.")


number_of_lines = 0
file_lines = lines[::-1]
list_time = (re.findall('.*\[(.*)\].*', (file_lines[0]))[0].split(' ')[0])
most_recent = datetime.datetime.strptime(list_time, '%d/%b/%Y:%H:%M:%S')
for line in file_lines:
    try:
        list_time = (re.findall('.*\[(.*)\].*', (line))[0].split(' ')[0])
        time_stamp = datetime.datetime.strptime(list_time, '%d/%b/%Y:%H:%M:%S')
        time_difference = most_recent - time_stamp
        if time_difference.days < 180 :
            number_of_lines +=1
        else:
            break
    except:
        pass
    
print ("The total number of requests in the last six months were " + str(number_of_lines))

fh.close()