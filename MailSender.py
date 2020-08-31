import json
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

toAddress = 'das.tamal00496@gmail.com'

with open('details.json', 'r') as data:
    json_data = json.load(data)
    userName = json_data['credentials']['userName']
    pwd = json_data['credentials']['password']

    smtp = json_data['smtpServer']['server']
    port = json_data['smtpServer']['port']

with open('msg.txt', 'r') as msg:
    mailMsg = msg.read()

'''Parsing the image file from classpath and read it as 
binary file and attaching to the multipart object'''

imgFile = 'light-house.jpg'
attachment = open(imgFile, 'rb')
p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())
encoders.encode_base64(p)
p.add_header('Content-Disposition', f'attachment; filename={imgFile}')

# Creating a MultiPart file which contatins all the details for the Mal

msg = MIMEMultipart()
msg['From'] = userName
msg['To'] = toAddress
msg['Subject'] = "Test Mail"
msg.attach(MIMEText(mailMsg, 'plain'))
msg.attach(p)

text = msg.as_string()

server = smtplib.SMTP(smtp, port)
try:
    server.starttls()
    server.login(userName, pwd)
    server.sendmail(userName, toAddress, text)
    print('Mail Sent')
except Exception as e:
    print('Exception occured with MSG -> %s' %e)
finally:
    server.quit()
