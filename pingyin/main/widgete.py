import requests
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import askURL
from requests import get
import pandas as pd

pinyin_sub = re.compile(r'<a class="pinyin_sub_idx"[^>]*>(.*?)</a>')
pinyin_link = re.compile(r'<a class="pinyin_sub_idx" href="([^"]+)"')
pinyin_in_sub = re.compile(
    r'<a\s+class="fontbox ff_yh"\s+href="[^"]*"\s+target="_blank">\s*<span\s+class="bihua">[^<]*<\/span>\s*[\u4e00-\u9fff]+<\/a>')


def main():
    url = "https://zd.hwxnet.com/pinyin.html"
    # 1.爬取网页
    datalist = getData(url)
    savepath = "pinyin2.xlsx"  # 当前目录新建XLS，存储进去
    # dbpath = "movie.db"              #当前目录新建数据库，存储进去
    # 3.保存数据
    saveData(datalist, savepath)  # 2种存储方式可以只选择一种
    # saveData2DB(datalist,dbpath)


# 爬取网页
def getData(url):
    datalist = []  # 用来存储爬取的网页信息
    html = askURL(url)  # 保存获取到的网页源码
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('a', class_="pinyin_sub_idx"):  # 查找符合要求的字符串
        data = []  # 保存一部电影所有信息
        item = str(item)
        sub = re.findall(pinyin_sub, item)  # 通过正则表达式查找
        chunks = [item + " " for item in sub]
        
        link = re.findall(pinyin_link, item)
        data.append(chunks)
        data.append(link)
        
        clean_urls = ''.join([url for url in link if url != [] and url != ''])
        print("clean_urls", clean_urls)
        uurl = askURL(str(clean_urls))
        ssoup = BeautifulSoup(uurl, "html.parser")
        for t in ssoup.find_all('div', class_="groupbox clearfix"):
            t = str(t)
            
            in_sub = re.findall(pinyin_in_sub, t)
            chunk = [t + "  " for t in in_sub]
            data.append(chunk)
        
        datalist.append(data)
    
    return datalist


# 得到指定一个URL的网页内容


# 保存数据到表格
def saveData(datalist, savepath):
    datalist = [list(zip(*item)) for item in datalist]
    
    df = pd.DataFrame(datalist, columns=["韵母", "链接", "字符"])
    df.to_excel(savepath, index=False, sheet_name='Sheet1')
    if datalist:  # 确保datalist不为空
        num_cols = len(datalist)

    else:
        num_cols = 0  # 如果datalis
    col = ("韵母", "链接", "字符")
    for i in range(0, 3):
       df.add([0, i, col[i]])
    for i in range(0, 410):
        print("第%d条" % (i + 1))  # 输出语句，用来测试
        data = datalist[i]
        # print(f"Data length: {len(data)}, i: {i}")
        sheet.write(i + 1, num_cols, data[i])
    for j in range(num_cols):
        sheet.write(i + 1, j, data[j])  # 数据
    book.save(savepath)  # 保存


# saveData(datalist, savepath)


def askURL(url):
    headers = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    try:
        response = get(url, headers=headers, timeout=30)
        response.raise_for_status()  # 如果响应状态码不是200，引发HTTPError异常
        html = response.text
        return html
    except requests.HTTPError as e:
        print(f"HTTPError: {e}")
    except requests.RequestException as e:
        print(f"RequestException: {e}")
    return ""


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    # init_db("movietest.db")
    print("爬取完毕！")
