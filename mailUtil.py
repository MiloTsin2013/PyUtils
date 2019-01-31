#!/usr/bin/env python
# -*- coding:utf-8 -*-

from email.mime.text import MIMEText
import smtplib
import logging

logging.basicConfig(filename='logger.log', level=logging.INFO, 
format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

class MailUtil(object):
    def __init__(self, sender=None, smtp_server=None, smtp_port=None, 
    user=None, password=None, receivers=None, title=None, content=None):
        '''
        sender          # 发件邮箱\n
        smtp_server     # 邮箱 SMTP 服务器\n
        smtp_port       # 服务器端口\n
        user            # 邮箱用户名\n
        password        # 邮箱密码\n
        receivers       # 收件人邮箱，若有多个使用列表形式\n
        title           # 邮件标题\n
        content         # 邮件内容\n
        '''
        self.sender = sender
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.user = user
        self.password = password
        self.to = self.parseTo(receivers)
        self.__mailInfo = self.getMailInfo_1(title, content)

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
        if isinstance(receivers, str):
            to = receivers
        return to

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
            smtp.sendmail(self.sender, self.to, self.__mailInfo)
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
            smtp.sendmail(self.sender, self.to, self.__mailInfo)
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
            smtp.sendmail(self.sender, to, self.__mailInfo)
        except Exception as e:
            logging.error(repr(e))
            flag = False
        finally:
            smtp.close()
        return flag

    def __str__(self):
        return f'sender={self.sender}, smtp_server={self.smtp_server}, smtp_port={self.smtp_port}, user={self.user}, password={self.password}, to={self.to}, mailInfo={self.__mailInfo}'     
        

if __name__ == "__main__":
    sender = "test@mail.com"        # 发件邮箱
    smtp_server = 'smtp.qq.com'     # 邮箱 SMTP 服务器
    smtp_port = '465'               # 服务器端口
    user = "test@mail.com"          # 邮箱用户名
    password = "*******"            # 邮箱密码
    to = "test@mail.com"            # 收件邮箱
    title = "hello"                 # 邮箱标题
    content = "Test python3 email"  # 邮箱内容
    
    mailUtil = MailUtil(sender, smtp_server, smtp_port, user, password, to, title, content)
    # print(mailUtil.mailInfo)
    # print(mailUtil)
    resulet = mailUtil.sendmail_SSL()
    print(resulet)
