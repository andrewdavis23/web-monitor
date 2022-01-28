import smtplib
import requests
import bs4

titles = []
titles_old = []
links = []
details = []
message = ''
any_new = False
new_count = 0

# user name and password
with open(r'C:\Python Programs\Web Monitor\UNAP.txt', 'r') as file:
    unap = file.read().split('\n')

# Gmail connection
server = smtplib.SMTP_SSL( 'smtp.gmail.com', 465 )
server.login( unap[0], unap[1] )

# access previous webpage
with open(r'C:\Python Programs\Web Monitor\OLDPAGE.txt', 'r') as file:
    wp_old = file.read()

# access current webpage
wp_new = requests.get('https://activities.outdoors.org/search/').text

# pull out piece of HTML that contains data
soup_old = bs4.BeautifulSoup(wp_old, 'html.parser')
soup_activities_old = soup_old.find(id='actdb-results')
soup_list_old = soup_activities_old.find_all(id='ListViewContent')

# extract hikes from old web page
for i in soup_list_old:
    titles_old.append(i.a.get_text())
    # links.append(i.a.get('href')[2:])
    # details.append(i.find('div', class_='details').get_text().replace('Activity',' | Activity'))

# pull out piece of HTML that contains data
soup_new = bs4.BeautifulSoup(wp_new, 'html.parser')
soup_activities_new = soup_new.find(id='actdb-results')
soup_list_new = soup_activities_new.find_all(id='ListViewContent')

# extract hikes from new web page and check for new hikes
for i in soup_list_new:
    title = i.a.get_text()

    if title not in titles_old:
        link = i.a.get('href')[2:]
        details_temp = i.find('div', class_='details').get_text().replace('Activity',' | Activity')
        dict_temp = {}
        for j in details_temp.split('|'):
            content = j.strip().partition(':')
            dict_temp[content[0].strip()] = content[2].strip()
        any_new = True
        new_count += 1
        titles.append(title)
        links.append(link)
        details.append(dict_temp)
        chunk = title +'\n'+ str(dict_temp) +'\n'+ link +'\n'*2
        chunk = chunk.replace(':','.')
        message += chunk

if any_new:
    print(message)

    # # replace cached webpage
    # with open(r'C:\Python Programs\Web Monitor\OLDPAGE.txt', 'w') as file:
    #     file.write(wp_new)

    # subscriber list
    with open(r'C:\Python Programs\Web Monitor\SUBS.txt', 'r') as file:
        rec_emails = file.read().split('\n')

    # add to email: subject and footnote
    plur = 's' if new_count > 1 else ''
    footnote = 'If you have any questions, comments, need to unsubscribe, reply to this email.'
    
    message = 'Subject: {} New Hike{} Posted!\n\n{}\n\n{}'.format(new_count,plur,message,footnote)

    server.sendmail(from_addr='Hike.Monitor@gmail.com', to_addrs=rec_emails, msg=message)
    server.quit()
else:
    print('NO NEW HIKES')

