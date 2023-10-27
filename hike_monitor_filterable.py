import smtplib
import requests
import bs4
import urllib3
import os
import re
import csv
from keep_alive import keep_alive
from time import sleep
from random import randint
from datetime import datetime, timedelta
# from replit import db

# HTTP server
keep_alive()
subs_fp = 'SUBS.txt'

def log(line):
  # adds text to the LOG file
  with open(r'LOG.txt', 'a') as file:
    file.writelines(line+'\n')
  print(line)

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

def el_tiempo():
  # used for log file
  now = a.strftime("%b.%-d %-I.%M %p")
  return now

def read_sub_file():
  """
  Loads the list of subscribers.
  Format: email, filter_option_1, filter_option_2, ...

  Will be replaced with repl database
  """
  dictionary = {}
    
  with open('SUBS.txt', 'r') as file:
      lines = file.readlines()
        
      headers = lines[0].strip().split(', ')
      values = [line.strip().split(', ') for line in lines[1:]]
      
      for header in headers:
          dictionary[header] = set()
      
      for value in values:
          for i in range(len(headers)):
              dictionary[headers[i]].add(value[i])
  
  return dictionary

def scrape_hike(h_id):
  """
  Scrapes the data for a hike.

  Args:
      h_id: Integer identify of the hike

  Returns:
      data: Dictionary containing the hike data for the   following data points:
            'Activity','Offered By','Status','Audience','Nearby AMC Destination'
  """
  url_template = 'https://activities.outdoors.org/search/index.cfm/action/details/id/'
  
  url = url_template + h_id
  
  wp_new = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, verify=False).text
  
  # pull out piece of HTML that contains data
  data = {}
  soup = bs4.BeautifulSoup(wp_new, 'html.parser')
  widget_text_divs = soup.find_all('div', class_='widgetText')
  
  for widget_text_div in widget_text_divs:
      headers = widget_text_div.find_all('h3')
      
      # ignore empty
      if len(headers) == 0:
          continue
  
      for header in headers:
  
          header_text = header.get_text()
          text_below_header = ""
          leader_count = 0
          next_element = header.find_next()
  
          if header_text == 'Leader':
              leader_count += 1
              if leader_count >= 1:
                  header_text = 'Leader ' + str(leader_count)
  
              script = soup.find('script', attrs={'data-cfasync': 'false'})
              script = script.next_sibling.get_text()
              matches = re.findall(r'(\w+) =', script) # all words followed by an equal sign
  
              values = {}
              for match in matches:
                  pattern = f"{match}\s*=\s*'(.+?)';" # create dict. of variable and value
                  value = re.search(pattern, script)
                  if value:
                      values[match] = value.group(1)
  
              text_below_header = values['first1'] + values['last1a'] + values['last1b']
  
              data[header_text] = text_below_header
  
  
          elif header_text =='Difficulty':
              anchor = header.parent.find('a')
              text_below_header += anchor.get_text()
  
  
          elif header_text in ['Activity','Offered By','Status','Audience','Nearby AMC Destination']:
              text_below_header += header.next_sibling.strip()
  
          data[header_text] = text_below_header
          next_element = next_element.find_next()
  
  # Print the extracted data dictionary
  print(data)
  return data
  
while True:
  collected_data = {}
  message = ''
  email = 'Hike.Monitor@gmail.com'
  psw = os.environ[email]
  server = 'smtp.gmail.com'
  port1 = '465'
  port2 = '587'
  soup_list_new = ['placeholder']
  page_num = 1
  a = datetime.today() - timedelta(hours=5)

  # Open cache of hike ids accumulated from previous runs
  with open(r'OLD_HIKES.txt', 'r') as file:
    old_hikes = file.read().split('\n')

  # login to Gmail
  try:
      server = smtplib.SMTP_SSL( server, port1 )
      server.login( email, psw )
  except:
      server = smtplib.SMTP_SSL( server, port2 )
      server.login( email, psw )

  # while the page contents exist, pull from page and go to next page
  log('++ {} ++ Pulling Pages'.format(el_tiempo()))
  
  while True:
  # loops through each page until 404 error

    
    wp_new = requests.get('https://activities.outdoors.org/search?mode=tile&pg='+str(page_num), headers={'User-Agent': 'Mozilla/5.0'}).text
     
    # pull out piece of HTML that contains data
    soup_new = bs4.BeautifulSoup(wp_new, 'html.parser')
    soup_activities_new = soup_new.find(id='actdb-results')
    soup_list_new = soup_activities_new.find_all(id='ListViewContent')

    with open(r'HTML_SAMPLE.txt', 'w') as file:
      file.writelines(line+'\n')
    print(line)

      # # breaks on 404 error
      # if len(soup_list_new) == 0:
      #     break

    ###############################################
      if page_num == 2:
            break

      # extract hikes from new web page and check for new hikes
      for i in soup_list_new:
          title = i.a.get_text()
          link = i.a.get('href')[2:]
          id = re.findall('id\/\d+',link)[0].replace('id/','')

          details_temp = i.find('div', class_='details').get_text().replace('Activity',' | Activity')
          dict_temp = {}
          dict_temp['Title'] = title

          for j in details_temp.split('|'):
              content = j.strip().partition(':')
              dict_temp[content[0].strip()] = content[2].strip()

          dict_temp['url'] = link

          # collected_data
          #nested dictionary containing data for collected hikes
          # KEYS: id > Title, Status, Date(s), Activity, Offered By, url
          collected_data[id] = dict_temp
      
      # ping at random intervals
      page_wait = randint(1,5)
      page_wait = page_wait/100
      sleep(page_wait)

      page_num += 1

  log( '{}:\n{} hikes pulled from {} pages.'.format(el_tiempo(),len(collected_data),page_num) )

  new_hikes = set(collected_data) - set(old_hikes)
  count_new_hikes = len(new_hikes)

  # add filters here
  if count_new_hikes > 0:
    plur = 's' if count_new_hikes > 1 else ''
    log( '{} new hike{} found.'.format(count_new_hikes,plur) )

  # replace cached webpage
  with open(r'OLD_HIKES.txt', 'w') as file:
        file.writelines('%s\n' % hike for hike in list(collected_data))

  # scrape data for new hikes
  # new_hikes_dict = [hike id][header]
  # headers = ['Activity','Offered By','Status','Audience','Nearby AMC Destination','Difficulty','Leader' or 'Leader 1, Leader 2, etc...']
  new_hikes_dict = {}  
  log('Scraping data from new hikes...')
  for h_id in new_hikes:
    new_hikes_dict[h_id] = scrape_hike(h_id)
  log('Scrape finished')

  # log the unique values for each header
  filterable = ['Activity','Offered By','Status','Audience','Nearby AMC Destination','Difficulty']
  filt_val = {} # filterable values in new data
  
  for header in filterable:
    filt_val[header] = set()
    
  for hike in new_hikes_dict:
    for header in filterable:
      filt_val[header].add(hike[header])
      
  # read the SEL.txt file
  filt_old = read_sub_file()

  # combine
  for header in filterable:
    filt_val[header].add(filt_old[header])
  
  # Save the accumulated options to be used in writing subscriptions on the website

  # for each subscriber [email,chapter1,chapter2,...] in [sub1,sub2,...] check
  for sub in subs:  
    message = '{},\n\n'.format(sub[0])
    subs_hike_count = 0
    for h_id in new_hikes:
      if collected_data[h_id]['Offered By'] in set(sub[1:]):
        subs_hike_count += 1
        chunk = ''
        for header, data in collected_data[h_id].items():
            chunk += '\n {} {} '.format(header.upper(), data)
        chunk = chunk.replace(':','.')
        message += chunk + '\n'

    # subscriber list
    subs = read_csv_file(subs_fp)

    # if the subscriber has a new hike posted, write email. Plur is used for punctuation
    if subs_hike_count > 0:
      plur = ''
      if subs_hike_count > 1:
        plur = 's'

      # remove any non-ascii characters
      e = message.encode('ascii',errors='ignore')
      message = e.decode()
  
      # add to email: subject and footnote
      chapters = ', '.join(chapter for chapter in sub[1:])
      
      footnote = '\nYou are subscribed to any new hikes from {}.\n\nIf you have any questions, comments, need to unsubscribe, reply to this email.\n'.format(chapters)
  
      subject = '{} hike{} found on {}'.format(subs_hike_count,plur,el_tiempo())
      
      message = 'Subject: {} \n\n{}\n\n{}'.format(subject,message,footnote)
  
      server.sendmail(from_addr=email, to_addrs=sub[0], msg=message)
      server.quit()
    else:
      log('No new hikes for {}'.format(sub[0]))

  # run process at random intervals
  wait = randint(100,120)
  log('Waiting for {} minutes...'.format(wait))
  sleep(60*wait)
  

