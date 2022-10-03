from datetime import datetime, date, time, timedelta
from skpy import Skype
from skpy import SkypeEventLoop
from skpy import SkypeNewMessageEvent
from skpy import SkypeUtils
from skpy import SkypeConnection
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import configparser
import logging
import time
import sys

password_protect = True
skype_username = 'mail@domen.com'
skype_password = 'password'
skype_status = 'Online'
email_username = 'mail@domen.com'
email_password = 'password'
email_notify = True
conn_expired = None

logging.basicConfig(level=logging.INFO, filename='skypedelivery.log', filemode='w', format='%(asctime)s %(message)s', datefmt='%d.%m.%y %H:%M:%S')

class Error(Exception):
    """Base class for other exceptions"""
    pass
class TokenExpired(Error):
    """Token expired"""
    pass    

def status_console(ok = True):
    if ok:
        sys.stdout.write('OK\r')
    else:
        sys.stdout.write('!\r')
    sys.stdout.flush()

def config_read():
    global skype_username, skype_password, skype_status , email_username, email_password, email_notify, password_protect
    config = configparser.RawConfigParser()
    config.read('skypedelivery.ini')
    skype_username = config.get('SKYPE', 'skype_username')
    skype_status = config.get('SKYPE', 'skype_status')
    email_username = config.get('EMAIL', 'email_username')
    email_notify = config.getboolean('EMAIL', 'email_notify')
    password_protect = config.getboolean('COMMON', 'password_protect')
    if password_protect == False:
        skype_password = config.get('SKYPE', 'skype_password')
        email_password = config.get('EMAIL', 'email_password')
    else:
        print('skype access:')
        skype_password = getpass()
        print('email access:')
        email_password = getpass()

def sendEMail(subject, text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_username, email_password)
    message = MIMEText(text.encode('utf-8'), _charset='UTF-8')
    message['Subject'] = Header(subject.encode('utf-8'), "utf-8")
    server.sendmail(email_username, email_username, message.as_string())
    server.quit()

    
class MySkype(SkypeEventLoop):
    def setPresence(self, status='Onlain'):
        self.conn("PUT", "{0}/users/ME/presenceDocs/messagingService".format(self.conn.msgsHost),
                  auth=SkypeConnection.Auth.RegToken, json={"status": status})
    def onEvent(self, event):
        if (conn_expired - datetime.now()).seconds < 3600:
            raise TokenExpired
        if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId:
            msg_time = datetime.now().strftime('%d.%m.%y %H:%M')
            msg_text = event.msg.content
            msg_from = event.msg.userId
            msg_print_text = '{0}\n\n{1}\n\n{2}'.format(msg_time, msg_text, msg_from)
            msg_print_title = 'SKYPE: {0}'.format(msg_from)
            print(msg_print_text)
            logging.info(msg_print_text)
            if email_notify == True:
                try:
                    sendEMail(msg_print_title, msg_print_text)
                    logging.info(msg_print_title)
                except Exception:
                    logging.error('send e-mail failed')


def connect():
    global conn_expired
    while(True):
        try:
            logging.info('try to connect')
            sk = MySkype(skype_username, skype_password)
            conn_expired = sk.conn.tokenExpiry['reg']
            logging.info('token registration until {0}'.format(sk.conn.tokenExpiry['reg'].strftime('%d.%m.%Y %H:%M')))            
            sk.setPresence(skype_status)
            logging.info('connected')
            status_console(True)
            sk.loop()
        except TokenExpired as inst:
            logging.info('token expired')
            status_console(False)
        except Exception as inst:
            logging.error(format(inst))
            status_console(False)
            time.sleep(10)


config_read()
connect()
