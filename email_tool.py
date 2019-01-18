from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email.utils import parseaddr, formataddr
import random
import smtplib


class Email(object):
    # 获取多个发送者信息，每个发送者以tuple(email_address,password,smtp_server,port)存储，
    # 每次发送邮件会随机从里面选择一个邮箱发送
    __senders = list()
    # 传入多个接收address
    __send_to_addresses = list()
    # 传入信息
    __message = "默认信息"
    # 封面显示标题
    __message_title = "默认标题"
    # 显示发件人
    __message_sender_name = "发送者"

    # 获取senders的用户信息
    def get_senders(self):
        return self.__senders

    def get_send_to_addresses(self):
        return self.__send_to_addresses

    def set_senders(self, senders):
        self.__senders = senders

    def set_send_to_addresses(self, send_to_addresses):
        self.__send_to_addresses = send_to_addresses

    def get_range_sender_info(self):
        return random.choice(self.__senders)

    # 发送简单信息，不带附件
    def send_easy_email(self):
        # 格式化内容
        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        sender = self.get_range_sender_info()

        sender_address = sender[0]
        sender_password = sender[1]
        smtp_server = sender[2]
        smtp_port = sender[3]
        message = MIMEText(self.__message, 'plain', 'utf-8')
        # 显示发件人名和发件地址
        message['From'] = _format_addr(self.__message_sender_name + '<%s>' % sender_address)
        # 标题
        message['Subject'] = Header(self.__message_title, 'utf-8').encode()

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.set_debuglevel(1)
        # 登录
        server.login(sender_address, sender_password)
        # 邮件发送
        server.sendmail(sender_address, self.__send_to_addresses, message.as_string())
        server.quit()

    # 发送一个附件，传入文件名，文件必须在该目录
    def send_file(self, file_name):
        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        sender = self.get_range_sender_info()

        sender_address = sender[0]
        sender_password = sender[1]
        smtp_server = sender[2]
        smtp_port = sender[3]

        message = MIMEMultipart()

        message.attach(MIMEText(self.__message, 'plain', 'utf-8'))
        # 显示发件人名和发件地址
        message['From'] = _format_addr(self.__message_sender_name + '<%s>' % sender_address)
        # 标题
        message['Subject'] = Header(self.__message_title, 'utf-8').encode()
        # 传入附件名
        attach = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')
        attach["Content-Type"] = 'application/octet-stream'
        attach["Content-Disposition"] = 'attachment; filename="' + file_name + '"'
        message.attach(attach)

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.set_debuglevel(1)
        # 登录
        server.login(sender_address, sender_password)
        # 邮件发送
        server.sendmail(sender_address, self.__send_to_addresses, message.as_string())
        server.quit()

    # 发送多个附件，传入文件的名字列表，文件必须在该目录
    def send_files(self, file_names):
        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        sender = self.get_range_sender_info()

        sender_address = sender[0]
        sender_password = sender[1]
        smtp_server = sender[2]
        smtp_port = sender[3]

        message = MIMEMultipart()

        message.attach(MIMEText(self.__message, 'plain', 'utf-8'))
        # 显示发件人名和发件地址
        message['From'] = _format_addr(self.__message_sender_name + '<%s>' % sender_address)
        # 标题
        message['Subject'] = Header(self.__message_title, 'utf-8').encode()

        for file_name in file_names:
            attach = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')
            attach["Content-Type"] = 'application/octet-stream'
            attach["Content-Disposition"] = 'attachment; filename="' + file_name + '"'
            message.attach(attach)

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.set_debuglevel(1)
        # 登录
        server.login(sender_address, sender_password)
        # 邮件发送
        server.sendmail(sender_address, self.__send_to_addresses, message.as_string())
        server.quit()


if __name__ == '__main__':
    email_tool = Email()
    # 可以从数据库中获取
    senders = [('', '', '', 465), ]
    # 从数据库中获取需要发送的列表，但是获取后就保存在内存中，如果新添加，通过某个接口刷新获取或者从重启服务
    email_tool.set_send_to_addresses(['', ''])

    email_tool.set_senders(senders)
    email_tool.send_files(['test.txt', 'test2.txt'])
