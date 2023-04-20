import smtplib
import datetime

from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import logging as log

class mail_sender:

    configs = {
        "outlook": {"address": "smtp-mail.outlook.com", "port": 587},
        "gmail": {"address": "smtp.gmail.com", "port": 587},
        "yahoo": {"address": "smtp.mail.yahoo.com", "port": 587},
    }


    def __init__(self, smtp_address="", smtp_port="", smtp_username="", smtp_passwd="", email_from="", autologin=True, config=None):

        self.smtp_username = smtp_username
        self.smtp_passwd = smtp_passwd
        self.email_from = email_from
        self.autologin = autologin
        # Si une config est précisée on écrase le smtp_address et smtp_port
        if config is not None:
            if config not in self.configs:
                raise ValueError("Invalid config name")
            else:
                self.smtp_address = self.configs[config]["address"]
                self.smtp_port = self.configs[config]["port"]
        else:
            self.smtp_address = smtp_address
            self.smtp_port = smtp_port


    def login(self, username=None, passwd=None):
        """ Login au serveur smtp """

        if username is None:
            username = self.smtp_username
        if passwd is None:
            passwd = self.smtp_passwd

        self.smtp_server = smtplib.SMTP( self.smtp_address,  self.smtp_port)
        self.smtp_server.ehlo()
        self.smtp_server.starttls()
        self.smtp_server.ehlo()
        try:
            self.smtp_server.login(username, passwd)
        except:
            log.exception("Erreur de login de l'email")
            return False
        else:
            return True



    def logout(self):
        """ Logout du serveur smtp """

        self.smtp_server.quit()


    def send_mail(self, email_to, email_subject, email_message, email_cc=[], reply_to="", files=[], content_type="html", autologin=None):
        """ Envoyer un mail """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = COMMASPACE.join(email_to)
            msg['Cc'] = COMMASPACE.join(email_cc)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = email_subject
            if reply_to != "":
                msg.add_header('reply-to', reply_to)

            if content_type == "text":
                msg.attach(MIMEText(email_message))
            elif content_type == "html":
                email_message = email_message.replace("\n", "<br>")
                msg.attach(MIMEText(email_message, "html"))
            else:
                raise ValueError("Wrong content type")

            for path in files:
                part = MIMEBase('application', "octet-stream")
                with open(path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename={}'.format(Path(path).name))
                msg.attach(part)

            if (autologin != None and autologin) or (autologin == None and self.autologin):
                if not self.login():
                    return False
            self.smtp_server.sendmail(self.email_from, tuple(email_to) + tuple(email_cc), msg.as_string())
            if (autologin != None and autologin) or (autologin == None and self.autologin):
                self.logout()
            return True
        except:
            log.exception("Erreur de lenvoi de l'email")
            return False
