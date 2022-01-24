from itertools import count
import smtplib
from datetime import datetime

server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()
server.login( 'Hike.Monitor@gmail.com', 'HikeMonitor@123' )

now = str(datetime.now())
msg = 'Message sent at '+now+' using less secure access and 1-digit'

server.sendmail( 'Hike.Monitor@gmail.com', '12034489920@tmomail.com', msg)

print(msg)