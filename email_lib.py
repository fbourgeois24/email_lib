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


    def send_mail(self, email_to, email_subject, email_message, content_type='text/plain'):
        """ Envoyer un mail 
            content_type:
                - text/plain
                - text/html
        """
        if content_type == 'text/plain':
            line_return = "\n"
        elif content_type == 'text/html':
            line_return = "<br>"

        message = "Content-Type: {}; charset=utf-8".format(content_type)
        message += line_return + "Content-Disposition: inline"
        message += line_return + "Content-Transfer-Encoding: 8bit"
        message += line_return + "From: {}".format(self.email_from)
        message += line_return + "To: {}".format(email_to)
        message += line_return + "Date: {}".format(datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'))
        message += line_return + "X-Mailer: python"
        message += line_return + "Subject: {}".format(email_subject) + line_return # .replace('\n','').replace('\r','')
        message += line_return + email_message

        print(message)

        self.smtp_server.sendmail(self.email_from, email_to, message.encode("utf-8"))

