import asyncio
import re  # 正则表达式，进行文字匹配`

import aiohttp
import requests
import xlwt  # 进行excel操
from bs4 import BeautifulSoup  # 网页解析，获取数据

pinyin_sub = re.compile(r'<a class="pinyin_sub_idx"[^>]*>(.*?)</a>')
pinyin_link = re.compile(r'<a class="pinyin_sub_idx" href="([^"]+)"')
pinyin_in_sub = re.compile(r'</span>([^<]*)</a>')


async def main():
    url = "https://zd.hwxnet.com/pinyin.html"
    # 1.爬取网页
    datalist = await getData(url)
    savepath = "pinyin3.xls"  # 当前目录新建XLS，存储进去
   
    await saveData(datalist, savepath)  # 2种存储方式可以只选择一种
  
async def run_main():
    await main()
# 爬取网页
async def getData(url):
    datalist = []  # 用来存储爬取的网页信息
    html_contents_async =await fetch_all_async([url]) # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html_contents_async[0], "html.parser")
    for item in soup.find_all('a', class_="pinyin_sub_idx"):  # 查找符合要求的字符串
        data = []  # 保存一部电影所有信息
        item = str(item)
        sub = re.findall(pinyin_sub, item)
        chunks = [item + " " for item in sub]  # 通过正则表达式查找
        link = re.findall(pinyin_link, item)
        data.append(chunks)
        data.append(link)
        clean_urls = ''.join([url for url in link if url != [] and url != ''])
        print("clean_urls", clean_urls)
        uurl_async=await fetch_all_async([clean_urls])
        ssoup = BeautifulSoup(uurl_async[0], "html.parser")
        for t in ssoup.find_all('div', class_="groupbox clearfix"):
            t = str(t)
            in_sub = re.findall(pinyin_in_sub, t)
            chunk = [t + "  " for t in in_sub]
            data.append(chunk)
        
        datalist.append(data)
    
    return datalist


# 得到指定一个URL的网页内容
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


# 保存数据到表格
async def saveData(datalist, savepath):
    if not datalist:
        print("No data to save.")
        return
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    
   
    cols = ("韵母", "链接","5轻声","阴平","阳平声","上声","去声")
    for i, col in enumerate(cols):
        sheet.write(0, i, col)
    for row_num, data in enumerate(datalist, start=1):
        for col_num, value in enumerate(data):
            sheet.write(row_num, col_num, value)
    book.save(savepath)  # 保存


async def askURL_async(session, url):
    session = requests.Session()
    headers = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.text()
    except aiohttp.ClientError as e:
        print(f"ClientError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return ""


async def fetch_all_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [askURL_async(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    asyncio.run(run_main())
    print("爬取完毕！")
