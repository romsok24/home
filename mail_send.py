# - *- coding: utf- 8 - *-
import smtplib

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 465
MAIL_USR = "xxxx@example.com"
MAIL_PASS = "xxxxxxxx"
message = """\
Sprawdź poziom pelletu w zasobniku
Zasypu wystarczy tylko na ok 1.5 dnia palenia, liczac od pierwszego komunikatu!

Pozdro
Twoja Kotłownia"""


sent_from = MAIL_USR
to = ['mail1@example.com', 'mail2@example.com']
subject = 'Sprawdź poziom pelletu w zasobniku'
subject = subject.encode('utf-8')
body = message.encode('utf-8')

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    smtp_server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    smtp_server.ehlo()
    smtp_server.login(MAIL_USR, MAIL_PASS)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
except Exception as ex:
    print ("Something went wrong….",ex)
