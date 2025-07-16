import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# 加载页面链接
with open("taiwu_wiki_links.json", "r", encoding="utf-8") as f:
    wiki_links = json.load(f)

# 准备已抓取过的链接（避免重复）
output_file = "taiwu_wiki_pages.jsonl"
fetched_urls = set()
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                fetched_urls.add(obj["url"])
            except:
                pass  # 防止某行解析失败

# 启动 Selenium
service = Service(r'C:\Users\21293\Desktop\taiwu_exe\chromedriver-win64\chromedriver.exe')
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 生产模式下推荐开启
driver = webdriver.Chrome(service=service, options=chrome_options)

with open(output_file, "a", encoding="utf-8") as f_out:
    for i, url in enumerate(wiki_links):
        if url in fetched_urls:
            print(f"✅ 已抓取过，跳过：{url}")
            continue

        try:
            print(f"📘 抓取第 {i+1}/{len(wiki_links)} 页：{url}")
            driver.get(url)
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            content_div = soup.find("div", class_="mw-parser-output")
            if content_div:
                text = content_div.get_text(separator="\n", strip=True)
                record = {"url": url, "text": text}
                json.dump(record, f_out, ensure_ascii=False)
                f_out.write("\n")
            else:
                print("⚠️ 没找到页面内容，跳过")
        except Exception as e:
            print(f"❌ 抓取失败：{url}\n错误信息：{e}")
            continue

driver.quit()
print(f"\n✅ 所有页面处理完毕，结果保存到 {output_file}")
