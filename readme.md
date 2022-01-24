# Web Monitoring Project
## Problem
This program will notify users of a website of any changes to that website.  The program may be specifically tailored to a website, especially if interpage navigation is needed.  I will be using this program to notify myself of updates to the Appalachian Mountain Club's activities page.  This website does not offer email notifications of new postings.

## Solution Steps
1) Program will run 24/7 on a rented server.
2) Pull webpage every half hour.
3) Compare new webpage to previous webpage and store new text.
4) Send the new text to a list of emails.

## Notes
### smtplib
- Messages are being sent through a gmail account
- SMS nor MMS is being received to my phone through ###########@tmomail.net.  No error messages are shown.  This isn't working via the program or manual email.  Will have to try with another number, otherwise it's a dead end.
- Emails sent are blank unless all special characters are removed.
### web scrape
- Previous issues using the scrapy module.  Had to create a seperate enviornment for it.
### web server
- Modules
