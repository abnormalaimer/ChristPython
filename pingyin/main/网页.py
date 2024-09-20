import requests
from docx import Document
from bs4 import BeautifulSoup
import re
findfirst = re.compile(r'<a class="fontbox ff_yh"[^>]*>(.*?)</a>')
def main():
    baseurl = "https://zd.hwxnet.com/pinyin.html"  # 要爬取的网页链接
    # 1.爬取网页
    writeword(baseurl)


def writeword(baseurl):
    # 使用requests获取网页内容
    for i in range(97, 123):
        letter = chr(i)
        print(letter)
        html = baseurl[:-5] + "/"+letter + ".html"
        print(html)
        response = requests.get(html)
        html_content = response.text
        
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 创建一个新的Word文档
        doc = Document()
        
        # 提取网页内容并写入Word文档
        for tag in soup.find_all('div', class_="groupbox clearfix"):
            first = re.findall(findfirst, tag)
            for match in  first:
                doc.add_paragraph(str(match))
            print(first)
            str1=str(first)+".docx"
            # 保存文档
            doc.save(str1)


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    # init_db("movietest.db")
    print("爬取完毕！")
