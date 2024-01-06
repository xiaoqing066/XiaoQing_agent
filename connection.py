import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from netmiko import ConnectHandler

usermail='xiaoqing066@tom.com'
password='xiaoqing066'
smtpserver='smtp.tom.com'
smtpport='25'
alert_mail='xiaoqing066@qq.com'

class Net:
    def __init__(self, device_type, host, username, password):
        self.device_info = {
            "device_type": device_type,
            "ip" : host, 
            "port" : 22, 
            "username" : username,
            "password" : password,
        }
        self.device=self.connect()

    def connect(self):
        return ConnectHandler(**self.device_info)
    
    def reconnect(self):
        self.device.disconnect()
        self.device=self.connect()
    
    def to_json(self,data_dict,file_path):
        with open(file_path,'w') as f:
            json.dump(data_dict,fp=f,indent=4)
    
    def send_mail(self, subject, body):
        message = MIMEText(body, 'html', 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = usermail
        message['To'] = alert_mail
        sender = smtplib.SMTP(smtpserver, smtpport)
        sender.login(usermail, password)
        sender.sendmail(usermail, alert_mail, message.as_string())
        sender.quit()   

