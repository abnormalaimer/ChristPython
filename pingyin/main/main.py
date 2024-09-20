import re  # 正则表达式，进行文字匹配`
import urllib.error  # 制定URL，获取网页数据
import urllib.request

import xlwt  # 进行excel操作
from bs4 import BeautifulSoup  # 网页解析，获取数据

pinyin_sub = re.compile(r'<a class="pinyin_sub_idx"[^>]*>(.*?)</a>')


def main():
	url = "https://zd.hwxnet.com/pinyin.html"
	# 1.爬取网页
	datalist = getData(url)
	savepath = "pinyin.xls"  # 当前目录新建XLS，存储进去
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
	for item in soup.find_all('div', class_="divright"):  # 查找符合要求的字符串
		data = []  # 保存一部电影所有信息
		item = str(item)
		link = re.findall(pinyin_sub, item)  # 通过正则表达式查找
		chunks = [item + " " for item in link]
		print(chunks)
		data.append(chunks)
		datalist.append(data)
	
	return datalist


# 得到指定一个URL的网页内容


# 保存数据到表格
def saveData(datalist, savepath):
	print("save.......")
	book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
	sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
	# col = ("sub")
	# for i in range(0, 50):
	#     sheet.write(0, i, col[i])  # 列名
	
	if datalist:  # 确保datalist不为空
		num_cols = len(datalist[0])
	else:
		num_cols = 0  # 如果datalis
	for i in range(0, 23):
		print("第%d条" % (i + 1))  # 输出语句，用来测试
		data = datalist[i]
		print(data)
		for j in range(num_cols):
			sheet.write(i, j, data[j])  # 数据
	book.save(savepath)  # 保存


def askURL(url):
	head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
		"User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
	}
	# 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
	
	request = urllib.request.Request(url, headers=head)
	html = ""
	try:
		response = urllib.request.urlopen(request)
		html = response.read().decode("utf-8")
	except urllib.error.URLError as e:
		if hasattr(e, "code"):
			print(e.code)
		if hasattr(e, "reason"):
			print(e.reason)
	return html


if __name__ == "__main__":  # 当程序执行时
	# 调用函数
	main()
	# init_db("movietest.db")
	print("爬取完毕！")
