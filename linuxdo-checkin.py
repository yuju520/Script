import os
import time
import random
import io
import requests
import sys
from tabulate import tabulate
from playwright.sync_api import sync_playwright

# 创建一个StringIO对象
output = io.StringIO()

# 将sys.stdout重定向到StringIO对象
sys.stdout = output

#Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

#Linux Do账号密码
USERNAME = os.environ.get("LD_USERNAME")
PASSWORD = os.environ.get("LD_PASSWORD")


HOME_URL = "https://linux.do/"


class LinuxDoBrowser:
    def __init__(self) -> None:
        self.pw = sync_playwright().start()
        self.browser = self.pw.firefox.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto(HOME_URL)

    def login(self):
        self.page.click(".login-button .d-button-label")
        time.sleep(2)
        self.page.fill("#login-account-name", USERNAME)
        time.sleep(2)
        self.page.fill("#login-account-password", PASSWORD)
        time.sleep(2)
        self.page.click("#login-button")
        time.sleep(10)
        user_ele = self.page.query_selector("#current-user")
        if not user_ele:
            print("Login failed")
            return False
        else:
            print("Check in success")
            return True

    def click_topic(self):
        max_attempts = 3  # 设置最大尝试次数为3
        attempt_count = 0  # 初始化尝试计数器

        for topic in self.page.query_selector_all("#list-area .title"):
            if attempt_count >= max_attempts:  # 如果尝试次数已达到最大值，则退出循环
                break

            new_page = self.context.new_page()
            new_page.goto(HOME_URL + topic.get_attribute("href"))
            time.sleep(3)  # 等待页面加载

            if random.random() < 0.02:  # 有2%的概率执行点赞操作
                self.click_like(new_page)
            attempt_count += 1  # 增加尝试计数器

            time.sleep(3)  # 等待操作完成
            new_page.close()  # 关闭新页面


    def run(self):
        if not self.login():
            return
        self.click_topic()
        self.print_connect_info()

    def click_like(self, page):
        page.locator(".discourse-reactions-reaction-button").first.click()
        print("Like success")

    def print_connect_info(self):
        page = self.context.new_page()
        page.goto("https://connect.linux.do/")
        rows = page.query_selector_all("table tr")

        info = []

        for row in rows:
            cells = row.query_selector_all("td")
            if len(cells) >= 3:
                project = cells[0].text_content().strip()
                current = cells[1].text_content().strip()
                requirement = cells[2].text_content().strip()
                info.append([project, current, requirement])

        print("--------------Connect Info-----------------")
        print(tabulate(info, headers=["项目", "当前", "要求"], tablefmt="pretty"))

        page.close()


if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("Please set USERNAME and PASSWORD")
        exit(1)
    l = LinuxDoBrowser()
    l.run()

# 获取输出文本
output_text = output.getvalue()

# 重定向sys.stdout回原始控制台
sys.stdout = sys.__stdout__

# 使用Telegram API发送消息
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": output_text,
    "parse_mode": "Markdown"  # 可选，如果你的消息中包含Markdown格式
}

response = requests.post(url, json=data)

# 检查请求是否成功
if response.ok:
    print("消息发送成功")
else:
    print("发送失败", response.text)
