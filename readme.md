# Web Page Monitoring Project
## Problem
This program will notify users of a website of any changes to a web page on that site.  The program may be specifically tailored to a website, especially if interpage navigation is needed.  I will be using this program to notify myself of updates to my local hiking club's activities page.  This website does not offer email notifications of new postings.

## Solution Steps
1) Program will run 24/7 on a rented server.
2) Pull web page at random intervals between 5 to 15 minutes.
3) Compare new web page to previous web page and store new text.
4) Send the new text to a list of emails.

## Notes
### smtplib
- SMS works when sent through email format: 'Subject: subject \n\nbody'
- Emails sent are blank unless all ":" are removed. May be more characters too.
- .sendmail returns error if any characters are not ASCII
### web scrape
- Previous issues using the scrapy module.  Had to create a seperate enviornment for it.
- Using the requests module and beautiful soup
### web server
- [REPL IT](http://www.replit.com) to host code and HTTP server
- [Up Time Robot](http://www.uptimerobot.com) to keep REPL server from sleeping and monitor failure
### unresolved issues
- REPL has been randomly dropping modules, possibly after server is down for extended time
- So far, only downtime is caused by failure of SMTP connection to gmail
