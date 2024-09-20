import aiohttp
import asyncio

from aiohttp import ClientSession
from bs4 import BeautifulSoup
import xlwt
import re

pinyin_sub = re.compile(r'<a class="pinyin_sub_idx"[^>]*>(.*?)</a>')
pinyin_link = re.compile(r'<a class="pinyin_sub_idx" href="([^"]+)"')
pinyin_in_sub = re.compile(r'<a\s+class="fontbox ff_yh"\s+href="[^"]*"\s+target="_blank">\s*<span\s+class="bihua">[^<]*<\/span>\s*[\u4e00-\u9fff]+<\/a>')

async def fetch(ClientSession, url):
    async with ClientSession.get(url) as response:
        return await response.text()

async def main():
    url = "https://zd.hwxnet.com/pinyin.html"
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        datalist = await parse_page(html)
        
        savepath = "pinyin2.xls"
        saveData(datalist, savepath)




async def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    datalist = []
    
    for item in soup.find_all('a', class_="pinyin_sub_idx"):
        data = []
        item_str = str(item)
        sub = re.findall(pinyin_sub, item_str)
        link = re.findall(pinyin_link, item_str)
        data.append([item + " " for item in sub])
        data.append(link)
        
        clean_urls = ''.join([url for url in link if url])
        if clean_urls:
            uurl = await fetch(ClientSession, clean_urls)
            ssoup = BeautifulSoup(uurl, "html.parser")
            for t in ssoup.find_all('div', class_="groupbox clearfix"):
                t_str = str(t)
                in_sub = re.findall(pinyin_in_sub, t_str)
                data.append([t_str + "  " for t in in_sub])
        
        datalist.append(data)
    
    return datalist



def saveData(datalist, savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    col = ("韵母", "链接", "字符")
    for i in range(3):
        sheet.write(0, i, col[i])
    
    row = 1
    for data in datalist:
        for item in data:
            for i, value in enumerate(item):
                sheet.write(row, i, value)
            row += 1
    
    book.save(savepath)
    print("Data saved successfully!")

if __name__ == "__main__":
    asyncio.run(main())
    print("爬取完毕！")
