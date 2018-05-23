'''
Title
------
sendgrid.py

Description
------------
Send emails for new users or forgotten passwords

'''

import sendgrid
import os
from sendgrid.helpers.mail import *

# make sure that you have this environment variable set on your machine
sendgrid_api_key = os.environ['SENDGRID_API_KEY']
sg = sendgrid.SendGridAPIClient(apikey=sendgrid_api_key)

def newUserEmail(username, password, email):
    html = '<h3>Thank you for creating a new account. Here are your credentials.</h3><h4><b>username: </b>' + username + '</h4><h4><b>password: </b>' + password + '<h5>Please sign in at this link: http://uw-database.herokuapp.com/</h5>'

    from_email = Email("achievementclub@unitedway.com")
    to_email = Email(email)
    subject = "Welcome to the Achievement Club Portal"
    content = Content("text/html", html)
    mail = Mail(from_email, subject, to_email, content)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
        if response.status_code != 200:
            print "Error sending email to user " + username
    except Exception as e:
        print "Error sending email to user " + username
        print e.message

