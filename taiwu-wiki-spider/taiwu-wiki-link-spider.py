from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import json

# 设置 chromedriver 路径
service = Service(r'C:\Users\21293\Desktop\taiwu_exe\chromedriver-win64\chromedriver.exe')
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 跑完再加这个节省时间

driver = webdriver.Chrome(service=service, options=chrome_options)

base_url = "https://taiwu.huijiwiki.com"
home_url = urljoin(base_url, "/wiki/首页")

# 打开首页
driver.get(home_url)
time.sleep(5)  # 等待 JS 加载完成

# 解析 HTML
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
content_div = soup.find("div", class_="mw-parser-output")

# 提取所有子链接
wiki_links = set()

if content_div:
    for a in content_div.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/wiki/") and not href.startswith("/wiki/Special:") and ':' not in href[6:]:
            wiki_links.add(urljoin(base_url, href))
    print("✅ 发现页面数：", len(wiki_links))
else:
    print("❌ 没找到主体内容div")

# 关闭浏览器
driver.quit()

# 保存链接到本地 json 文件
with open("taiwu_wiki_links.json", "w", encoding="utf-8") as f:
    json.dump(sorted(list(wiki_links)), f, ensure_ascii=False, indent=2)

print("✅ 所有页面链接已保存到 taiwu_wiki_links.json")
