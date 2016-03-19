#useful stuff


def read_certain_line(file_name,file_loc,linenumber):
  pwd_file = file_loc + file_name
  open_file = open(pwd_file)
  pwd_read = open_file.readlines()
  #pwd_mail = "".join(pwd_read.split())
  open_file.close()
  return pwd_read[linenumber]


def send_mail(to_addr, subject, body,password):
  import smtplib
  from email.mime.text import MIMEText
  from email.mime.multipart import MIMEMultipart
  
  from_addr = 'python.mailing.bot@gmail.com'

  msg = MIMEMultipart()
  msg['From'] = from_addr
  msg['To'] = to_addr
  msg['Subject'] = subject 
  msg.attach(MIMEText(body,'plain','utf-8'))
  msg_final = msg.as_string().encode('ascii')


  # Credentials (if needed)
  username = 'python.mailing.bot@gmail.com'

  # The actual mail send
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(from_addr, to_addr, msg_final)
  server.quit()
