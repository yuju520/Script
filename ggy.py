import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 配置邮件发送者和接收者
sender_email = "发信邮箱"
receiver_email = "收信邮箱"
password = "发信邮箱授权码或者密码"

# 页面 URL
url = "https://www.ggy.net/register.php"

def check_page():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text()
        if "暂停新用户注册" not in page_text:
            send_email()
        else:
            print("还没开放。");
    else:
        print("Failed to retrieve the webpage.")

def send_email():
    subject = "咕咕云 开放了注册！"
    body = f"快快点击： {url} 去注册账号吧！"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.qq.com', 25)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

if __name__ == "__main__":
    check_page()
