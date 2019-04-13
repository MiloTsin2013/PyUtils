#!/usr/bin/env python
# -*- coding:utf-8 -*-

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
import smtplib
import logging

logging.basicConfig(filename='logger.log', level=logging.INFO, 
format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

class MailUtil(object):
    def __init__(self, sender=None, smtp_server=None, smtp_port=None, user=None, password=None, 
    receivers=None, cc_receivers=None ,title=None, content=None, annexs=None):
        '''
        sender          # 发件邮箱\n
        smtp_server     # 邮箱 SMTP 服务器\n
        smtp_port       # 服务器端口\n
        user            # 邮箱账户\n
        password        # 邮箱密码\n
        receivers       # 收件人邮箱，使用列表形式\n
        cc_receivers    # 抄送邮箱，使用列表形式\n
        title           # 邮件标题\n
        content         # 邮件内容\n
        annexs          # 邮件附件，附件路径，使用列表形式\n
        '''
        self.sender = sender
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.user = user
        self.password = password
        self.to = self.parseTo(receivers)
        self.cc_to = self.parseTo(cc_receivers)
        self.all_to = receivers + cc_receivers
        self.__mailInfo = self.getMailInfo(title, content, annexs)

    @property
    def mailInfo(self):
        return self.__mailInfo

    @mailInfo.setter
    def mailInfo(self, value):
        self.__mailInfo = value

    def parseTo(self, receivers):
        to = None
        if isinstance(receivers, list):
            to = ';'.join(receivers)
        return to

    def getMailInfo(self, title, content, annexs):
        message = MIMEMultipart()
        message['From'] = Header(self.sender, 'utf-8')
        message['To'] =  Header(self.to, 'utf-8')
        message['Cc'] = Header(self.cc_to, 'utf-8')
        message['Subject'] = Header(title, 'utf-8')
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        if isinstance(annexs, list):
            for annex in annexs:
                # 构造附件
                att = MIMEBase('application', 'octet-stream')
                att.set_payload(open(annex, 'rb').read())
                att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', annex) )
                encoders.encode_base64(att)
                message.attach(att)
        return str(message)

    def getMailInfo_1(self, title, content):
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = self.sender   # 发送者
        msg['To'] = self.to         # 接收者
        msg['Subject'] = title
        # message = msg.as_string()
        message = str(msg)
        return message

    def getMailInfo_2(self, title, content):
        # header = 'To:' + self.to + '\n' + 'From: ' + self.sender + '\n' + 'Subject:' + title + '\n'
        # message = header + '\n '+ content
        message = f'To:{self.to}\nFrom:{self.sender}\nSubject:{title}\n\n{content}'
        return message
        
    '''连接 SMTP 服务器，根据服务器所支持的方法，在明文/SSL/TLS三种方式中选择一种'''
    def sendmail(self):
        flag = True
        # smtp = None
        try:
            # 普通方式，通信过程不加密
            smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
            smtp.ehlo()  # 声明用户认证
            # 登录
            smtp.login(self.user, self.password)
            # 发送邮件
            smtp.sendmail(self.sender, self.all_to, self.__mailInfo)
        except Exception as e:
            logging.error(repr(e))
            flag = False
        finally:
            smtp.close()
        return flag
    
    def sendmailWithoutLogin(self):
        flag = True
        # smtp = None
        try:
            # 普通方式，通信过程不加密
            smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
            smtp.starttls()
            # 发送邮件
            smtp.sendmail(self.sender, self.all_to, self.__mailInfo)
        except Exception as e:
            logging.error(repr(e))
            flag = False
        finally:
            smtp.close()
        return flag

    def sendmail_TLS(self):
        flag = True
        smtp = None
        try:
            # TLS加密方式，通信过程加密，邮件数据安全
            smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
            smtp.set_debuglevel(True)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            # 登录
            smtp.login(self.user, self.password)
            # 发送邮件
            smtp.sendmail(self.sender, self.all_to, self.__mailInfo)
        except Exception as e:
            logging.error(repr(e))
            flag = False
        finally:
            smtp.close()
        return flag

    def sendmail_SSL(self):
        flag = True
        try:
            # SSL加密方式，通信过程加密，邮件数据安全
            smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            smtp.ehlo()
            # 登录
            smtp.login(self.user, self.password)
            # 发送邮件
            smtp.sendmail(self.sender, self.all_to, self.__mailInfo)
        except Exception as e:
            logging.error(repr(e))
            flag = False
        finally:
            smtp.close()
        return flag

    def __str__(self):
        return f'sender={self.sender}, smtp_server={self.smtp_server}, smtp_port={self.smtp_port}, password={self.password}, to={self.to}, mailInfo={self.__mailInfo}'     
        

if __name__ == "__main__":
    sender = "endruz@foxmail.com"       # 发件邮箱
    smtp_server = 'smtp.qq.com'         # 邮箱 SMTP 服务器
    smtp_port = '465'                   # 服务器端口
    user = "endruz@foxmail.com"         # 邮箱账户
    password = "****************"       # 邮箱密码
    to = ["endruz9334@gmail.com"]       # 收件邮箱
    cc_to = ['endruz@foxmail.com']      # 抄送邮箱
    title = "hello"                     # 邮箱标题
    content = "Test python3 email"      # 邮箱内容
    annexs = ['logger.log']             # 附件
    
    mailUtil = MailUtil(sender, smtp_server, smtp_port, user, password, to, cc_to, title, content, annexs=annexs)
    # print(mailUtil.mailInfo)
    # print(mailUtil)
    resulet = mailUtil.sendmail_SSL()
    print(resulet)