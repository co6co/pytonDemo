import smtplib
from email.mime.text import MIMEText

def sendMail(user,pwd,to,subject,text):
    msg = MIMEText(text)
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject
    try:
        
        #POP3服务器: pop.163.com
        #SMTP服务器: smtp.163.com
        #IMAP服务器: imap.163.com

        smtpServer = smtplib.SMTP('smtp.163.com',25) # 25、587、465、2525
        print("[+] Connecting To Mail Server.")
        smtpServer.ehlo()
        print("[+] Starting Encrypted Session.")
        smtpServer.starttls()
        smtpServer.ehlo()
        print("[+] Logging Into Mail Server.")
        smtpServer.login(user, pwd)
        print("[+] Sending Mail.")
        smtpServer.sendmail(user, to, msg.as_string())
        smtpServer.close()
        print("[+] Mail Sent Successfully.")
    except Exception as e:
        print("[-] Sending Mail Failed.",e)
user = 'ynchyung@163.com'
pwd = 'KJIJJQWN3QJWRRP'
sendMail(user, pwd, 'ynchyung@163.com', 'Re: Important', 'Test Message')
