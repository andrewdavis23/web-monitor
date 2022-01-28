import bs4

titles = []
links = []
details = []
message = ''

with open('C:\Python Programs\Web Monitor\OLDPAGE.html', 'r') as file:
    wp_old = file.read()

soup = bs4.BeautifulSoup(wp_old, 'html.parser')

soup_activities = soup.find(id='actdb-results')

soup_list = soup_activities.find_all(id='ListViewContent')

soup_map = soup.find_all('script')[15]


print(soup_map)

# for i in soup_list:
#     titles.append(i.a.get_text())
#     links.append(i.a.get('href')[2:])
#     details_temp = i.find('div', class_='details').get_text().replace('Activity',' | Activity')
#     dict_temp = {}
#     for j in details_temp.split('|'):
#         content = j.strip().partition(':')
#         dict_temp[content[0].strip()] = content[2].strip()
#     details.append(dict_temp)

# for i in range(len(titles)):
#     chunk = titles[i] +'\n'+ str(details[i]) +'\n'+ links[i] +'\n'*2
#     chunk = chunk.replace(':','.')
#     message += chunk

print(message)

# for i in details:
#     for j in i.split('|'):
#         print(j.strip().partition(':'))