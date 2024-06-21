import requests
import re
import urllib.parse
import sys  # 引入 sys 模块

# 定义 cookie
cookie = ''

# 第一个请求
url1 = "https://www.yueing.org/home.php?id=1&mod=task&do=apply"
headers1 = {
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
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
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
        "Sec-Fetch-Mode": "navigate",
        "Host": "www.yueing.org",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Sec-Fetch-Dest": "document",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": cookie
    }
    response2 = requests.get(url2, headers=headers2)
    print(response2.text)
