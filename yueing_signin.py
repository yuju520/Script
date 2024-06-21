from curl_cffi import requests
import re
import os
import urllib.parse
from bs4 import BeautifulSoup

# 你的Telegram机器人的API token
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN","")
# 接收消息的聊天ID
chat_id = os.environ.get("CHAT_ID","")
# 构建Telegram API URL
telegram_api_url = os.environ.get("TELEGRAM_API_URL","https://api.telegram.org") # 代理api,可以使用自己的反代

# 定义一个请求TG函数
def telegram_Bot(telegram_bot_token,chat_id,message):
    url = f'{telegram_api_url}/bot{telegram_bot_token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    r = requests.post(url, json=data)
    response_data = r.json()
    return response_data['ok']  # 修改：将 msg 作为返回值

# 定义 cookie
cookie = os.environ.get("YY_COOKIE","")

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
    message = "抱歉，本期您已申请过此任务，请下期再来"
# 调用函数并接收返回值
    result = telegram_Bot(telegram_bot_token, chat_id, message)

# 打印返回值
    print(f"telegram推送结果：{result}\n")  # 修改：使用 result 而不是 msg

else:
    # 第二个请求
    url2 = "https://www.yueing.org/home.php?do=draw&mod=task&id=1&item=doing"
    response2 = requests.get(url2, headers=headers1)
    # print(response2.text)

# 第三个请求
url3 = "https://www.yueing.org/home.php?mod=space&do=notice&view=system"
response3 = requests.get(url3, headers=headers1)
html_content = response3.text
soup = BeautifulSoup(html_content, 'html.parser')
time_ago = soup.select_one('span.xg1.xw0 span').get_text(strip=True)
task_completion = ' '.join([item for item in soup.select_one('dd.ntc_body').stripped_strings if '查看我的积分' not in item])
# print(f'{time_ago}，{task_completion}')
message2 = f'{time_ago}，{task_completion}'
result2 = telegram_Bot(telegram_bot_token, chat_id, message2)
