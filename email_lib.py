import smtplib
import datetime


class mail_sender:

    def __init__(self, smtp_address, smtp_port, smtp_username, smtp_passwd, email_from, autologin=True):

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
        self.smtp_server.ehlo()
        self.smtp_server.starttls()
        self.smtp_server.ehlo()

        self.smtp_server.login(username, passwd)


    def logout(self):
        """ Logout du serveur smtp """

        self.smtp_server.quit()


    def send_mail(self, email_to, email_subject, email_message):
        """ Envoyer un mail """

        message = "Content-Type: text/html; charset=utf-8"
        message += "\nContent-Disposition: inline"
        message += "\nContent-Transfer-Encoding: 8bit"
        message += "\nFrom: {}".format(self.email_from)
        message += "\nTo: {}".format(email_to)
        message += "\nDate: {}".format(datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'))
        message += "\nX-Mailer: python"
        message += "\nSubject: {}\n".format(email_subject.replace('\n','').replace('\r',''))
        message += "\n" + email_message

        self.smtp_server.sendmail(self.email_from, email_to, message.encode("utf8"))

