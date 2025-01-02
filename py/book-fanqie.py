import time
 
import bs4
import requests
import re
import lxml
 
 
url = 'https://fanqienovel.com/page/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5',
    # 其他自定义的请求头信息
}
 
response = requests.get(url, headers=headers)
 
soup = bs4.BeautifulSoup(response.text, 'lxml')
 
 
CODE_ST = 58344
CODE_ED = 58715
charset = ['D', '在', '主', '特', '家', '军', '然', '表', '场', '4', '要', '只', 'v', '和', '?', '6', '别', '还', 'g',
           '现', '儿', '岁', '?', '?', '此', '象', '月', '3', '出', '战', '工', '相', 'o', '男', '首', '失', '世', 'F',
           '都', '平', '文', '什', 'V', 'O', '将', '真', 'T', '那', '当', '?', '会', '立', '些', 'u', '是', '十', '张',
           '学', '气', '大', '爱', '两', '命', '全', '后', '东', '性', '通', '被', '1', '它', '乐', '接', '而', '感',
           '车', '山', '公', '了', '常', '以', '何', '可', '话', '先', 'p', 'i', '叫', '轻', 'M', '士', 'w', '着', '变',
           '尔', '快', 'l', '个', '说', '少', '色', '里', '安', '花', '远', '7', '难', '师', '放', 't', '报', '认',
           '面', '道', 'S', '?', '克', '地', '度', 'I', '好', '机', 'U', '民', '写', '把', '万', '同', '水', '新', '没',
           '书', '电', '吃', '像', '斯', '5', '为', 'y', '白', '几', '日', '教', '看', '但', '第', '加', '候', '作',
           '上', '拉', '住', '有', '法', 'r', '事', '应', '位', '利', '你', '声', '身', '国', '问', '马', '女', '他',
           'Y', '比', '父', 'x', 'A', 'H', 'N', 's', 'X', '边', '美', '对', '所', '金', '活', '回', '意', '到', 'z',
           '从', 'j', '知', '又', '内', '因', '点', 'Q', '三', '定', '8', 'R', 'b', '正', '或', '夫', '向', '德', '听',
           '更', '?', '得', '告', '并', '本', 'q', '过', '记', 'L', '让', '打', 'f', '人', '就', '者', '去', '原', '满',
           '体', '做', '经', 'K', '走', '如', '孩', 'c', 'G', '给', '使', '物', '?', '最', '笑', '部', '?', '员', '等',
           '受', 'k', '行', '一', '条', '果', '动', '光', '门', '头', '见', '往', '自', '解', '成', '处', '天', '能',
           '于', '名', '其', '发', '总', '母', '的', '死', '手', '入', '路', '进', '心', '来', 'h', '时', '力', '多',
           '开', '己', '许', 'd', '至', '由', '很', '界', 'n', '小', '与', 'Z', '想', '代', '么', '分', '生', '口',
           '再', '妈', '望', '次', '西', '风', '种', '带', 'J', '?', '实', '情', '才', '这', '?', 'E', '我', '神', '格',
           '长', '觉', '间', '年', '眼', '无', '不', '亲', '关', '结', '0', '友', '信', '下', '却', '重', '己', '老',
           '2', '音', '字', 'm', '呢', '明', '之', '前', '高', 'P', 'B', '目', '太', 'e', '9', '起', '稜', '她', '也',
           'W', '用', '方', '子', '英', '每', '理', '便', '西', '数', '期', '中', 'C', '外', '样', 'a', '海', '们',
           '任']
 
#解析章节加密内容
def interpreter(cc):
    bias = cc - CODE_ST
    if charset[bias] == '?':
        return chr(cc)
    return charset[bias]
 
#获取小说章节内容
def funLog(text):
    soup = bs4.BeautifulSoup(text.text, 'lxml')
    novel = soup.find('div', class_='muye-reader-content noselect')
    p1 = ''
    for p in novel.children:
        text = p.get_text()
        length = len(text)
        for ind in range(length):
            cc = ord(text[ind])
            ch = text[ind]
            if CODE_ST <= cc <= CODE_ED:
                ch = interpreter(cc)
            p1 += ch
    return p1
 
def extract_chatper_titles(html_content):
    pattern = r'title\":\"(.*?)\"'
    titles = re.findall(pattern,html_content)
    return titles
 
def Htltle(text):
    novel = text.find('h1').text
    return novel
 
#"div.volume.volume_first + div.chapter > div.chapter-item"
 
#print(page_text)
a = time.time()
dir_path = 'D:\资料库\测试爬虫'
 
 
def Run(id):
    response = requests.get(url+id, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    li_list = soup.select(
        "div.chapter-item"
    )
    total = len(li_list)
    titles = extract_chatper_titles(response.text)
    for i,div in enumerate(li_list):
        title = div.a.string
        detail_url = "https://fanqienovel.com"+div.a["href"]
        #print(detail_url)
        response = requests.get(url=detail_url,headers=headers)
        #print(response.text)
        content = funLog(response)  # 获取章节内容
        with open("../static/" + Htltle(soup) + ".txt", 'a',encoding='utf-8') as f:
            f.write('{}\n'.format(titles[i+1]))
            f.write(content)
            f.write('\n\n\n')
            print('已下载{}'.format((i + 1) / len(titles)))
    time.sleep(0.2)  # 每隔200毫秒爬取一章
 
def Main():
    str = input("输入小说id")
    Run(str)
    print('下载完成')
    b = time.time()
    print('用时{}'.format(b - a))
 
Main()