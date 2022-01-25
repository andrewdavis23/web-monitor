import smtplib
from datetime import datetime
import requests
import bs4

titles = []
links = []
details = []
message = ''
any_new = False
new_count = 0

# Gmail connection
server = smtplib.SMTP_SSL( 'smtp.gmail.com', 465 )
server.login( 'Hike.Monitor@gmail.com',************************)

# access previous webpage
with open('C:\Python Programs\Web Monitor\OLDPAGE.txt', 'r') as file:
    wp_old = file.read()

# access current webpage
wp_new = requests.get('https://activities.outdoors.org/search/').text

# pull out piece of HTML that contains data
soup_old = bs4.BeautifulSoup(wp_old, 'html.parser')
soup_activities_old = soup_old.find(id='actdb-results')
soup_list_old = soup_activities_old.find_all(id='ListViewContent')

# extract hikes from old web page
for i in soup_list_old:
    titles.append(i.a.get_text())
    links.append(i.a.get('href')[2:])
    details.append(i.find('div', class_='details').get_text())

################################### test ######################################
print('OLD HIKES\n',titles)

# pull out piece of HTML that contains data
soup_new = bs4.BeautifulSoup(wp_new, 'html.parser')
soup_activities_new = soup_new.find(id='actdb-results')
soup_list_new = soup_activities_new.find_all(id='ListViewContent')

# extract hikes from new web page and check for new hikes
for i in soup_list_new:
    title_i = i.a.get_text()
    link_i = i.a.get('href')[2:]
    details_i = i.find('div', class_='details').get_text()

    if title_i not in titles:
        any_new = True
        new_count += 1
        chunk = title_i +'\n'+ details_i +'\n'+ link_i +'\n'*2
        chunk = chunk.replace(':','.')
        chunk = chunk.replace('Activity',' | Activity')
        message += chunk

################################### test ######################################
print('any_new? ',str(any_new))

if any_new:
    # # replace cached webpage
    # with open('C:\Python Programs\Web Monitor\OLDPAGE.txt', 'w') as file:
    #     file.write(wp_new)

    # subscriber list
    with open('C:\Python Programs\Web Monitor\SUBS.txt', 'r') as file:
        rec_emails = file.read().split('\n')

    # add to email: subject and footnote
    plur = 's' if new_count > 1 else ''
    footnote = 'If you have any questions, comments, need to unsubscribe, reply to this email.'
    
    message = 'Subject: {} New Hike{} Posted!\n\n{}\n\n{}'.format(new_count,plur,message,footnote)

    ################################### test ######################################
    print(message)

    server.sendmail(from_addr='Hike.Monitor@gmail.com', to_addrs=rec_emails, msg=message)
    server.quit()

