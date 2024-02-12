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


    def __init__(self, smtp_address=None, smtp_port=None, smtp_username=None, smtp_passwd=None, email_from=None, reply_to=None, 
        autologin=None, config=None):
        """ Si une config est précisée on la lit et on l'écrase par les paramètres si précisés
            La config peut être de 2 types (si pas None) :
            1) str => nom de la config (voir dict configs plus haut)
            2) dict => contient les paramètres, clés possibles :
                - config => nom de la config (voir dict configs plus haut)
                - addr => smtp_address
                - port => smtp_port
                - user => smtp_username
                - passwd => smtp_passwd
                - from => email_from
                - reply_to
                - autologin => autologin
        """
        # On défini les variables à None
        self.smtp_address = None
        self.smtp_port = None
        self.smtp_username = None
        self.smtp_passwd = None
        self.email_from = None
        self.reply_to = None
        self.autologin = None

        # Si config spécifiée, on la lit
        if config is not None:
            # Si une config est spécifiée
            if type(config) == str and config in self.configs:
                self.smtp_address = self.configs[config]["address"]
                self.smtp_port = self.configs[config]["port"]
            elif type(config) == dict:
                # Pour addr et port, soit le nom de config est précisé dans config ou paramètre correspondant directement dans la config
                # On vérifie que toutes les clés sont connues
                for key in config.keys():
                    if key not in ("config", "addr", "port", "user", "passwd", "from", "reply_to", "autologin"):
                        raise ValueError(f"Clé '{key}' incorrecte dans la config !")

                self.smtp_address = self.configs[config.get("config", {})].get("address") or config.get("addr")
                self.smtp_port = self.configs[config.get("config", {})].get("port") or config.get("port")
                self.smtp_username = config.get("user")
                self.smtp_passwd = config.get("passwd")
                self.email_from = config.get("from")
                self.reply_to = config.get("reply_to")
                self.autologin = config.get("autologin")
            else:
                raise ValueError("Invalid config name or type")

       
        # On remplace les valeurs par les paramètres si existants
        self.smtp_address = self.smtp_address or smtp_address
        self.smtp_port = self.smtp_port or smtp_port
        self.smtp_username = self.smtp_username or smtp_username
        self.smtp_passwd = self.smtp_passwd or smtp_passwd
        self.email_from = self.email_from or email_from or self.smtp_username
        self.reply_to = self.reply_to or reply_to or self.smtp_username
        self.autologin = self.autologin or autologin
        if self.autologin == None: self.autologin = True

        # Si aucune valeur
        if self.smtp_address is None or self.smtp_port is None:
            raise ValueError("Il faut spécifier une config ou au minimum smtp_address et smtp_port")

    def login(self, username=None, passwd=None):
        """ Login au serveur smtp """

        if username is None:
            username = self.smtp_username
        if passwd is None:
            passwd = self.smtp_passwd

        self.smtp_server = smtplib.SMTP(self.smtp_address, self.smtp_port)
        self.smtp_server.ehlo()
        if self.smtp_server.has_extn('STARTTLS'):
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


    def send_mail(self, email_to, email_subject="", email_message="", email_from=None, email_cc=[], email_cci=[], reply_to=None, 
        files=[], content_type="html", autologin=None):
        """ Envoyer un mail """
        try:
            if type(email_to) == str:
                email_to = (email_to,)
            if type(email_cc) == str:
                email_cc = (email_cc,)
            msg = MIMEMultipart()
            msg['From'] = email_from or self.email_from
            msg['To'] = COMMASPACE.join(email_to)
            msg['Cc'] = COMMASPACE.join(email_cc)
            msg['Bcc'] = COMMASPACE.join(email_cci)
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = email_subject
            msg.add_header('reply-to', reply_to or self.reply_to)

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
            self.smtp_server.sendmail(self.email_from, tuple(email_to) + tuple(email_cc) + tuple(email_cci), msg.as_string())
            if (autologin != None and autologin) or (autologin == None and self.autologin):
                self.logout()
            return True
        except:
            log.exception("Erreur de lenvoi de l'email")
            return False
