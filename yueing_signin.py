import requests
import re
import urllib.parse
import sys  # 引入 sys 模块
from lxml import html
from bs4 import BeautifulSoup

# 定义 cookie
cookie = ''

# 第一个请求
url1 = "https://www.yueing.org/home.php?id=1&mod=task&do=apply"
headers1 = {
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Host": "www.yueing.org",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.yueing.org/home.php?mod=task",
    "Cookie": cookie
}
response1 = requests.get(url1, headers=headers1)

# 检查响应文本中是否包含特定的字符串
if "抱歉，本期您已申请过此任务，请下期再来" in response1.text:
    print("抱歉，本期您已申请过此任务，请下期再来")
    sys.exit()
elif "您已成功申请过此任务" in response1.text:
    # 第二个请求
    url2 = "https://www.yueing.org/home.php?do=draw&mod=task&id=1&item=doing"
    headers2 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.yueing.org/home.php?mod=task&do=draw&id=1",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "Sec-Fetch-Mode": "navigate",
        "Host": "www.yueing.org",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Sec-Fetch-Dest": "document",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": cookie
    }
    response2 = requests.get(url2, headers=headers2)
    # print(response2.text)

# 第三个请求
url3 = "https://www.yueing.org/home.php?mod=space&do=notice&view=system"
headers3 = {
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Host": "www.yueing.org",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.yueing.org/home.php?mod=task",
    "Cookie": cookie
}
response3 = requests.get(url3, headers=headers3)
html_content = response1.text

soup = BeautifulSoup(html_content, 'html.parser')
time_ago = soup.select_one('span.xg1.xw0 span').get_text(strip=True)
task_completion = ' '.join([item for item in soup.select_one('dd.ntc_body').stripped_strings if '查看我的积分' not in item])

print(f'{time_ago}，{task_completion}')
