import requests
from bs4 import BeautifulSoup

# 目标网页URL
url = 'https://www.dmit.io/cart.php'

# 发送HTTP GET请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取网页的文本内容
    text = soup.get_text(separator='\n', strip=True)
    
    # 定义关键词列表
    keywords = ['LAX.Pro.Wee', 'LAX.Pro.MALIBU', 'LAX.Pro.PalmSpring']
    
    # 检查文本中是否包含关键词
    found_keyword = next((keyword for keyword in keywords if keyword in text), None)
    
    if found_keyword:
        # 如果包含关键词，发送通知到Telegram
        telegram_token = 'YourToken'  # 替换为你的Telegram机器人token
        chat_id = 'YourId'                   # 替换为你的Telegram聊天ID
        
        # 准备POST请求的URL和数据
        telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        telegram_data = {
            'chat_id': chat_id,
            'text': f"{found_keyword}有货了",
            'parse_mode': 'Markdown'
        }
        
        # 发送POST请求到Telegram API
        telegram_response = requests.post(telegram_url, json=telegram_data)
        
        # 打印Telegram API的响应
        print("Telegram message sent successfully." if telegram_response.ok else "Failed to send message.")
        print(telegram_response.json())
    else:
        print(f"没有补货")
else:
    print(f"Failed to retrieve content, status code: {response.status_code}")
