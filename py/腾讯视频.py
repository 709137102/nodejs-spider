# 第1步：导入相关模块
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql
import random
import time
from selenium.webdriver.chrome.service import Service


# 第2步：打开腾讯视频
viewtype = "地球最牛黑科技"
driver_path = "C:\\Users\\cui peng fei\\Downloads\\ChromeDriver\\chromedriver.exe"
service = Service(executable_path=driver_path)
url = "https://v.qq.com/channel/tech/list?filter_params=itype%3D6%26icompany%3D-1%26icelebrity%3D-1%26icolumn%3D-1%26sort%3D40&page_id=channel_list_second_page"
# viewdriver = webdriver.Chrome(service=service)
viewdriver = webdriver.Chrome(executable_path=driver_path)
# viewdriver.get(url)

# 第3步：最大化浏览器窗口
viewdriver.maximize_window()

# 定义下拉滚动条函数
def pullscrool(driver, mintime, maxtime):
    # 腾讯视频页面屏蔽掉了滚动条，使用空格键下拉滚动条
    try:
        # 先定位一个按钮才能使用空格下拉滚动条
        tagx = driver.find_element_by_xpath('//div[@dt-eid="choose_item"][text()=" 最近热播 "]')
        tagx.click()
    except:
        pass
    # 先获取body元素，然后在该元素上面发送空格键
    tag = driver.find_element_by_tag_name("body")
    for count in range(35):
        # 模拟空格键下拉滚动条
        tag.send_keys(Keys.SPACE)
        time.sleep(random.uniform(mintime, maxtime))  # 取随机值更人性化


# 第4步：下拉滚动条
pullscrool(viewdriver, 0.03, 0.07)

# 第5步：爬取所有视频标签
viewstag = viewdriver.find_elements_by_class_name("horizontal")


# 定义一些变量
viewslist = []
viewcount = 0     # 当前已解析的视频数量
maxviewcount = 8  # 当天最大视频数量

# 定义存放视频名称，视频链接，视频图片，视频时长的列表
viewslist = []

# 连接数据库
gxviewdb = pymysql.connect(user='birdpython',   # 登录数据库的用户名（换成你自己的）
                           passwd='laoniao',    # 登录数据库的密码（换成你自己的）
                           db='gxview',         # 要操作的数据库（换成你自己的）
                           host='88.88.88.88',  # 登录数据库的IP地址（换成你自己的）
                           charset='utf8')      # 指定编码格式为utf-8，否则显示乱码


# 获取所有视频名称
cursor = gxviewdb.cursor()
sql = "select viewname from gxviewtable"
cursor.execute(sql)
gxviewdbnames = cursor.fetchall()
cursor.close()

# 筛选不符合时长的视频
viewmintime = "00:50"
viewmaxtime = "03:00"
def judgeviewtime(viewtime):
    if viewmintime <= viewtime <= viewmaxtime:
        return True
    else:
        return False

# 筛选重复的视频
def judgeviewrepeat(viewname):
    if viewname in gxviewdbnames:
        return False
    else:
        return True

# 第6步：提取每个视频的信息（视频名称，视频链接，视频图片，视频时长）
for item in viewstag:
    viewname = item.find_element_by_class_name('title').text.strip()                # 视频名称
    viewlink = item.get_attribute("href")                                           # 视频链接
    viewimg = "https:" + item.find_element_by_tag_name('img').get_attribute("src")  # 视频图片链接
    viewtime = item.find_element_by_class_name('right-bottom-text').text.strip()    # 视频时长

    # 去掉一些不友好的标点符号
    viewname = viewname.replace("\"", u"”") \
        .replace("\'", u"’").replace(":", u"：").replace("?", u"？") \
        .replace(" ", u"").replace("|", u"，").replace(u" ", u"") \
        .replace(u"❤", u"").replace(u"➕", u"").replace(u"#", u"") \
        .replace("/", u"-")

    if judgeviewtime(viewtime) and judgeviewrepeat((viewname,)):
        viewslist.append([viewname, viewlink, viewimg,  viewtime, viewtype])

        # 第7步：判断爬够8个视频，退出爬取腾讯视频逻辑
        viewcount += 1  # 每次循环已经解析过的视频个数加1
        if viewcount >= maxviewcount:  # 如果够8个就退出循环
            break

# 存储视频信息到数据库
for views in viewslist:
    sql = 'insert gxviewtable(viewname, viewlink, viewimglink, viewlength, viewtype)' \
          ' values ("%s", "%s", "%s", "%s", "%s")' % (views[0], views[1], views[2], views[3], views[4])
    cursor = gxviewdb.cursor()
    cursor.execute(sql)
    gxviewdb.commit()
    cursor.close()