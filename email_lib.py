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
        if autologin:
            self.login()


    def login(self, username=None, passwd=None):
        """ Login au serveur smtp """

        if username is None:
            username = self.smtp_username
        if passwd is None:
            passwd = self.smtp_passwd

        # Pour le tls
        # self.smtp_server.ehlo()
        self.smtp_server.starttls()
        self.smtp_server.ehlo()

        self.smtp_server.login(username, passwd)


    def logout(self):
        """ Logout du serveur smtp """

        self.smtp_server.quit()


    def send_mail(self, email_to, email_subject, email_message, email_cc=[], files=[]):
        """ Envoyer un mail 
            content_type:
                - text/plain
                - text/html
        """
        # if content_type == 'text/plain':
        #     line_return = "\n"
        # elif content_type == 'text/html':
        #     line_return = "<br>"

        # message = "Content-Type: {}; charset=utf-8".format(content_type)
        # message += line_return + "Content-Disposition: inline"
        # message += line_return + "Content-Transfer-Encoding: 8bit"
        # message += line_return + "From: {}".format(self.email_from)
        # message += line_return + "To: {}".format(email_to)
        # message += line_return + "Cc: {}".format(email_cc)
        # message += line_return + "Date: {}".format(datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'))
        # message += line_return + "X-Mailer: python"
        # message += line_return + "Subject: {}".format(email_subject) + line_return # .replace('\n','').replace('\r','')
        # message += line_return + email_message

        # self.smtp_server.sendmail(self.email_from, email_to + email_cc, message.encode("utf-8"))

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
        self.smtp_server.sendmail(self.email_from, email_to, msg.as_string())
        self.logout()


