import smtplib
import requests
import bs4
import os
from keep_alive import keep_alive
from time import sleep
from random import randint
from datetime import datetime

new_data = {}
message = ''
new_count = 0
psw = os.environ['Hike.Monitor@gmail.com']
soup_list_new = ['placeholder']
page_num = 1

# HTTP server
keep_alive()

while True:
  try:
      # Gmail connection
      server = smtplib.SMTP_SSL( 'smtp.gmail.com', 465 )
      server.login( 'Hike.Monitor@gmail.com', psw )
  except:
      sleep(10)
      # Gmail connection
      server = smtplib.SMTP_SSL( 'smtp.gmail.com', 465 )
      server.login( 'Hike.Monitor@gmail.com', psw )

  # access previous webpage
  with open(r'OLD_HIKES.txt', 'r') as file:
      old_hikes = file.read().split('\n')

  # while the page contents exist, pull from page and go to next page
  print(' ++ Pulling Pages ++')
  while True:
      wp_new = requests.get('https://activities.outdoors.org/search?mode=tile&pg='+str(page_num)).text

      # pull out piece of HTML that contains data
      soup_new = bs4.BeautifulSoup(wp_new, 'html.parser')
      soup_activities_new = soup_new.find(id='actdb-results')
      soup_list_new = soup_activities_new.find_all(id='ListViewContent')

      if len(soup_list_new) == 0:
          break

      # extract hikes from new web page and check for new hikes
      for i in soup_list_new:
          title = i.a.get_text()
          link = i.a.get('href')[2:]
          details_temp = i.find('div', class_='details').get_text().replace('Activity',' | Activity')
          dict_temp = {}

          for j in details_temp.split('|'):
              content = j.strip().partition(':')
              dict_temp[content[0].strip()] = content[2].strip()

          new_data[title] = [dict_temp,link]
      
      # ping at random intervals
      page_wait = randint(1,5)
      page_wait = page_wait/100
      sleep(page_wait)

      page_num += 1

  print('{} hikes pulled from {} pages'.format(len(new_data),page_num))

  new_hikes = set(new_data) - set(old_hikes)

  # create message from new_data FORMAT: new_data[title] = [dict_temp,link]
  # add filters here
  if len(new_hikes) > 0:
      print('{} new hikes found',format(len(new_hikes)))
      for h in new_hikes:
          chunk = h
          # for each dictionary of hike details (Status,Date(s),Activity,Offered by)
          for i in new_data[h][0]:
              chunk += '\n {} {} '.format(i.upper(),new_data[h][0][i])
          chunk += '\n'+ new_data[h][1] +'\n'*2
          chunk = chunk.replace(':','.')
          message += chunk

      # replace cached webpage
      with open(r'OLD_HIKES.txt', 'w') as file:
          file.writelines('%s\n' % hike for hike in new_hikes)

      # subscriber list
      with open(r'SUBS.txt', 'r') as file:
          rec_emails = file.read().split('\n')

      # add to email: subject and footnote
      footnote = 'If you have any questions, comments, need to unsubscribe, reply to this email.'
      
      message = 'Subject: New Hike Posted! \n\n{}\n\n{}'.format(message,footnote)

      server.sendmail(from_addr='Hike.Monitor@gmail.com', to_addrs=rec_emails, msg=message)
      server.quit()
  else:
      print('NO NEW HIKES '+str(datetime.now()))

  # run process at random intervals
  wait = randint(20,30)
  sleep(60*wait)
  print('Waiting for {} minutes.'.format(wait))

