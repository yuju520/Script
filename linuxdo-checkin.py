import os
import time
import random
import io
import requests
import sys
from tabulate import tabulate
from playwright.sync_api import sync_playwright

# 创建一个StringIO对象来捕获输出
output = io.StringIO()

# 将sys.stdout重定向到StringIO对象
sys.stdout = output

# Telegram Bot 配置
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Linux.do 账号密码
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
        self.visited_posts = 0  # 新增：记录访问的帖子数量

    def login(self):
        # 执行登录操作
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
            print("登录失败")
            return False
        else:
            print("签到成功")
            return True

    def click_topic(self):
        # 修改：随机访问5-10个帖子
        num_posts_to_visit = random.randint(5, 10)
        topics = self.page.query_selector_all("#list-area .title")
        
        for topic in random.sample(topics, min(num_posts_to_visit, len(topics))):
            new_page = self.context.new_page()
            new_page.goto(HOME_URL + topic.get_attribute("href"))
            time.sleep(3)  # 等待页面加载

            if random.random() < 0.02:  # 有2%的概率执行点赞操作
                self.click_like(new_page)
            
            self.visited_posts += 1  # 增加访问的帖子计数
            time.sleep(3)  # 等待操作完成
            new_page.close()  # 关闭新页面

        print(f"共访问了 {self.visited_posts} 个帖子")

    def run(self):
        if not self.login():
            return
        self.click_topic()
        self.print_connect_info()

    def click_like(self, page):
        page.locator(".discourse-reactions-reaction-button").first.click()
        print("点赞成功")

    def print_connect_info(self):
        # 打印连接信息
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
        print("请设置 USERNAME 和 PASSWORD 环境变量")
        exit(1)
    
    try:
        l = LinuxDoBrowser()
        l.run()
    except Exception as e:
        # 捕获并记录异常
        error_message = f"执行过程中发生错误: {str(e)}"
        print(error_message)
        sys.stdout = sys.__stdout__  # 恢复标准输出
        output_text = output.getvalue() + "\n" + error_message
    else:
        # 获取正常输出文本
        output_text = output.getvalue()
    finally:
        # 重定向 sys.stdout 回原始控制台
        sys.stdout = sys.__stdout__

    # 使用 Telegram API 发送消息
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
