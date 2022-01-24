import smtplib
import re
from datetime import datetime

server = smtplib.SMTP_SSL( 'smtp.gmail.com', 465 )
server.login( 'Hike.Monitor@gmail.com', 'HikeMonitor@123' )

now = str(datetime.now())

new_hikes = 'This message was sent at {}'.format(now)

message = re.sub('[^A-Za-z0-9 ]+', '', new_hikes)

rec_emails = ['Hike.Monitor@gmail.com', 'andrewdavis23@gmail.com', 'cleanloud444@gmail.com']

server.sendmail(from_addr='Hike.Monitor@gmail.com', to_addrs=rec_emails, msg=message)
server.quit()

