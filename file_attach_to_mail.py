import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "Enter your mail here"
toaddr = "Enter reciver mail here"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Report"

body = "Please FTA. Thank you."

msg.attach(MIMEText(body, 'plain'))

filename = "edcd.csv"
attachment = open("/home/race/edcd.csv", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "Enter your password here")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
