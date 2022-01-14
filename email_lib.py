import smtplib
import datetime

from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

class mail_sender:

    def __init__(self, smtp_address, smtp_port, smtp_username, smtp_passwd, email_from, autologin=False):

        self.smtp_server = smtplib.SMTP(smtp_address, smtp_port)
        self.smtp_username = smtp_username
        self.smtp_passwd = smtp_passwd
        self.email_from = email_from
        # Pour le tls
        self.smtp_server.ehlo()
        self.smtp_server.starttls()
        self.smtp_server.ehlo()
        if autologin:
            self.login()


    def login(self, username=None, passwd=None):
        """ Login au serveur smtp """

        if username is None:
            username = self.smtp_username
        if passwd is None:
            passwd = self.smtp_passwd

        self.smtp_server.login(username, passwd)


    def logout(self):
        """ Logout du serveur smtp """

        self.smtp_server.quit()


    def send_mail(self, email_to, email_subject, email_message, email_cc=[], files=[]):
        """ Envoyer un mail """

        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = COMMASPACE.join(email_to)
        msg['Cc'] = COMMASPACE.join(email_cc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = email_subject

        msg.attach(MIMEText(email_message))

        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(path).name))
            msg.attach(part)

        self.login()
        self.smtp_server.sendmail(self.email_from, email_to + email_cc, msg.as_string())