import smtplib
import re
from datetime import datetime
import requests
import bs4

# Gmail connection
server = smtplib.SMTP_SSL( 'smtp.gmail.com', 465 )
server.login( 'Hike.Monitor@gmail.com', 'HikeMonitor@123' )

# used for testing
now = str(datetime.now())

# access previous webpage
with open('C:\Python Programs\Web Monitor\OLDPAGE.txt', 'r') as file:
    wp_old = file.read().replace('\n', '')

# access current webpage
wp_new = requests.get('https://activities.outdoors.org/search/')

# replace cached webpage
with open('C:\Python Programs\Web Monitor\OLDPAGE.txt', 'r') as file:
    file.write(wp_new)

# extract activities list from HTML soup
# create list of activities

new_hikes = str(set(wp_new).difference(wp_old))

# some or all special characters will cause blank emails
message = re.sub('[^A-Za-z0-9 ]+', '', new_hikes)

# subscriber list (make external)
rec_emails = ['Hike.Monitor@gmail.com', 'andrewdavis23@gmail.com', 'cleanloud444@gmail.com']

server.sendmail(from_addr='Hike.Monitor@gmail.com', to_addrs=rec_emails, msg=message)
server.quit()

