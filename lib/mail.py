# -*- coding: utf-8 -*-  
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email.utils import COMMASPACE,formatdate
from email import encoders

import os

def send_mail(server, fro, to, subject, text, files=[]):
    #assert type(to) == list
    #assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['Subject'] = subject
    msg['To'] = to
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text))

    for file in files:
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
        part.set_payload(open(file, 'rb'.read()))
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    import smtplib
    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()
