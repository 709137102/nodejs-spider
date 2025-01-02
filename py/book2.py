import re
import requests
from lxml import etree

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

# 定义小说首页地址 https://www.biquai.cc/ https://www.bq04.cc/book/45361/
index_url = 'https://www.bq04.cc/book/45361/'

# 发送网络请求
response = requests.get(index_url, headers=headers)

# 筛选链接和标题
info_list = re.findall('<dd><a href ="(.*?)">(.*?)</a></dd>', response.text)

print(info_list)
# 去除前面6个数据
info_list = info_list[6:]

# 遍历列表，得到每章的部分链接和标题
for info in info_list:
    # 从元组中取出部分链接进行拼接，获取每章的页面链接
    url = 'https://www.bq04.cc' + info[0]
    print("url:"+url)
    # 获取数据
    response = requests.get(url, headers=headers)
    html_data = etree.HTML(response.text)

    # xpath筛选出文本数据，并将数据列表转换成字符串
    text_list = html_data.xpath('//div[@id="chaptercontent"]/text()')
    text = ''.join(text_list)

    # 添加标题行
    book_text = '\n\n' + info[1] + '\n\n'
    # 去除广告文本
    book_text += text.replace('请收藏本站：https://www.biquge11.cc。笔趣阁手机版：https://m.biquge11.cc ', '').replace('　　', '\n')

    print("正在下载：" + info[1])
    print(book_text)

    # 保存到文件
    with open('斗破苍穹.txt', 'a', encoding='utf-8') as file:
        file.write(book_text)
