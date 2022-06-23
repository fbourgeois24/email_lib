# email_lib
## Créer l'objet
```python
mail = email_lib.mail_sender(smtp_address, smtp_port, smtp_username, smtp_passwd, email_from, autologin=True, config=None
```
Pour une config personnalisée, utiliser
- smtp_address
- smtp_port
Pour une config existante, utiliser 'config'
Config existantes:
- outlook (address= "smtp-mail.outlook.com", port= 587)
- gmail (address: "smtp.gmail.com", port: 587)



## Envoyer un email
```python
mail.send_mail(email_to, email_subject, email_message, email_cc=[], reply_to="", files=[], content_type="html")
```
- content_type : défini le type de contenu du mail. Valeurs possibles : 'text' ou 'html' (html par défaut)
- 