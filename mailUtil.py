import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import logging

logging.basicConfig(filename='logger.log', level=logging.INFO)

def sendmail(receivers,title,content):
    '''
    receivers   # 收件人邮箱，若有多个使用列表形式\n
    title       # 邮件标题\n
    content     # 邮件内容\n
    '''
    flag = True
    # 发件邮箱信息
    sender = "test@mail.com"    # 发件邮箱
    smtp_server = 'smtp.qq.com'         # 邮箱 SMTP 服务器
    smtp_port = '465'                    # 服务器端口
    user = "test@mail.com"               # 邮箱用户名
    password = "******"       # 邮箱密码

    # 邮件内容
    to = ""
    if isinstance(receivers,list):
        to = ';'.join(receivers)
    else:
        to = receivers
    # 方法一
    # header = 'To:' + to + '\n' + 'From: ' + sender + '\n' + 'Subject:' + title + '\n'
    # message = header + '\n '+ content
    # 方法二
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = sender   # 发送者
    msg['To'] =  to        # 接收者
    msg['Subject'] = title
    message = msg.as_string()

    try:
        # 连接 SMTP 服务器，根据服务器所支持的方法，在明文/SSL/TLS三种方式中选择一种
        # 普通方式，通信过程不加密
        smtp = smtplib.SMTP(smtp_server,smtp_port)
        smtp.ehlo() # 声明用户认证
        # # TLS加密方式，通信过程加密，邮件数据安全
        # smtp = smtplib.SMTP(smtp_server,smtp_port)
        # smtp.set_debuglevel(True)
        # smtp.ehlo()
        # smtp.starttls()
        # smtp.ehlo()
        # # SSL加密方式，通信过程加密，邮件数据安全
        # smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        # smtp.ehlo()
        
        # 登录
        smtp.login(user, password)
        # 发送邮件
        smtp.sendmail(sender, to, message)
    except Exception as e:
        print(repr(e))
        flag = False
    finally:
        smtp.close()
    return flag

if __name__ == "__main__":
    mail = "test@mail.com"
    title = "hello"
    content = "Test python3 email"
    res = sendmail(mail,title,content)
    print(res)