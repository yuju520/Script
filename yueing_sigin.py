import requests
import re
import urllib.parse
import sys  # 引入 sys 模块

# 定义 cookie
cookie = 'BlEM_2132_saltkey=f6OT8EV2; BlEM_2132_did=lZPQ8QLp1FQq0Slf; BlEM_2132_lastvisit=1712804029; BlEM_2132_nofavfid=1; BlEM_2132_saltkey=I1eEj1mm; BlEM_2132_lastvisit=1711950315; BlEM_2132_nofavfid=1; BlEM_2132_smile=4D1; BlEM_2132_did=PS2cSL4sjpCgmCXM; BlEM_2132_ulastactivity=cc3eNkiuSONgImvyTTkbXDJcTa8%2BR7ElS28RRtm7HIQMn7ARohQe; BlEM_2132_lastcheckfeed=43250%7C1694522875; BlEM_2132_sid=Cz4Dv2; BlEM_2132_auth=d99a%2BaQpsns%2BpDzxZL3dymzyBDcpMuj5vHN%2FxSCgS2mgP9ux5UANBcqCs08uN060e1WojQi6jGNrZHec6DdCOifk7g; BlEM_2132_lastcheckfeed=43250%7C1715354843; BlEM_2132_st_t=43250%7C1715354942%7Cb8c3702f95a61f554b72e19bf91356f3; BlEM_2132_atarget=1; BlEM_2132_forum_lastvisit=D_59_1715354942; BlEM_2132_visitedfid=59; BlEM_2132_smile=4D1; BlEM_2132_viewid=tid_115672; BlEM_2132_clearUserdata=forum; BlEM_2132_st_p=43250%7C1715354986%7C6ecdce065dd208c631eec63c4b1b5ced; BlEM_2132_ulastactivity=870fB%2F7Cw3M10TnINFuKng1hsF5iXKJ0nsOvdkj5EmJc7C%2B8TkIj; BlEM_2132_lastact=1715355036%09home.php%09spacecp'

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
