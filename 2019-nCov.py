import requests
import re
from bs4 import BeautifulSoup
from time import sleep
import json
from prettytable import ALL
from prettytable import PrettyTable

hubei = {}
guangdong = {}
zhejiang = {}
beijing = {}
shanghai = {}
hunan = {}
anhui = {}
chongqing = {}
sichuan = {}
shandong = {}
guangxi = {}
fujian = {}
jiangsu = {}
henan = {}
hainan = {}
tianjin = {}
jiangxi = {}
shanxi1 = {} # 陕西
guizhou = {}
liaoning = {}
xianggang = {}
heilongjiang = {}
aomen = {}
xinjiang = {}
gansu = {}
yunnan = {}
taiwan = {}
shanxi2 = {} # 山西
jilin = {}
hebei = {}
ningxia = {}
neimenggu = {}
qinghai = {} # none
xizang = {} # none
provinces_idx = [hubei, guangdong, zhejiang, chongqing, hunan, anhui, beijing,
                 shanghai, henan, guangxi, shandong, jiangxi, jiangsu, sichuan,
                 liaoning, fujian, heilongjiang, hainan, tianjin, hebei, shanxi2,
                 yunnan, xianggang, shanxi1, guizhou, jilin, gansu, taiwan,
                 xinjiang, ningxia, aomen, neimenggu, qinghai, xizang]
map = {
    '湖北':0, '广东':1, '浙江':2, '北京':3, '上海':4, '湖南':5, '安徽':6, '重庆':7,
    '四川':8, '山东':9, '广西':10, '福建':11, '江苏':12, '河南':13, '海南':14,
    '天津':15, '江西':16, '陕西':17, '贵州':18, '辽宁':19, '香港':20, '黑龙江':21,
    '澳门':22, '新疆':23, '甘肃':24, '云南':25, '台湾':26, '山西':27, '吉林':28,
    '河北':29, '宁夏':30, '内蒙古':31, '青海':32, '西藏':33
}


def getTime(text):
    TitleTime = str(text)
    TitleTime = re.findall('<span>(.*?)</span>', TitleTime)
    return TitleTime[0]

def getAllCountry(text):
    AllCountry = str(text)
    AllCountry = AllCountry.replace("[<p class=\"confirmedNumber___3WrF5\"><span class=\"content___2hIPS\">", "")
    AllCountry = AllCountry.replace("<span style=\"color: #4169e2\">", "")
    AllCountry = re.sub("</span>", "", AllCountry)
    AllCountry = AllCountry.replace("</p>]", "")
    return AllCountry 

def clear(text):
    text = str(text)
    name = re.findall(': 32px;">(.*?)</span>', text)
    confirmed = re.findall('E7-fW">(.*?)</p>', text)
    dead = re.findall('ANk6l">(.*?)</p>', text)
    cure = re.findall('3mcDz">(.*?)</p>', text)
    
    if len(name) > 0 and name[0] == '武汉':
        confirmed.pop(0)
        dead.pop(0)
        cure.pop(0)
        return name, confirmed, dead, cure
    else:
        return name, confirmed, dead, cure

def query(province):
    table = PrettyTable(['地区', '确诊', '死亡', '治愈'])
    for (k,v) in province.items():
        name = k
        table.add_row([name, v[0] if v[0] != '' else '-', v[1] if v[1] != '' else '-', v[2] if v[2] != '' else '-'])
    if len(province.keys()) != 0:
        print(table)
    else:
        print("暂无")

def getConfirmedNumer(text):
    text = str(text)
    confirmedNumber = re.findall('<p class=\"subBlock2___E7-fW\">(.*?)</p>', text)
    if confirmedNumber[0] == "":
        return '-'
    return int(confirmedNumber[0])

def getCureNumber(text):
    text = str(text)
    cureNumber = re.findall('<p class=\"subBlock3___3mcDz\">(.*?)</p>', text)
    if cureNumber[0] == '':
        return '-'
    return int(cureNumber[0])

def getDeadNumer(text):
    text = str(text)
    deadNumber = re.findall('<p class=\"subBlock4___ANk6l\">(.*?)</p>', text)
    if deadNumber[0] == '':
        return '-'
    return int(deadNumber[0])

def getArea(text):
    text = str(text)
    area = re.findall('mCC\"/>(.*?)</p>', text)
    return area[0]

def getInfo(text):
    text = str(text)
    text = re.findall('/i>(.*?)</p>', text)
    return text[0]

def initMap(soup):
    provinces_info = soup.findAll("div", class_="areaBlock1___3V3UU")
    idx = 0
    provinces_info = str(provinces_info)
    province = re.findall("uQmCC\"/>(.*?)</p><p", provinces_info)
    for i in range(len(province)):
        map[province[i]] = i
        

def main():
    url = "https://3g.dxy.cn/newh5/view/pneumonia"

    #  try:
    headers = {}
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36' #http头大小写不敏感
    headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text,'lxml')
    table = PrettyTable(['地区', '确诊', '死亡', '治愈'])
    table.hrules = ALL

    #### 截至时间
    TitleTime = getTime(soup.select('.mapTitle___2QtRg'))
    
    print()
    print("                     ",TitleTime + "\n")
    print("==================================全国数据==================================")
    AllCountry = getAllCountry(soup.select('.confirmedNumber___3WrF5'))
    print("\n" + AllCountry + "\n")

    print("==================================相关情况==================================")
    print()
    infos = soup.findAll("p", class_='descList___3iOuI')
    for info in infos:
        info = getInfo(info)
        print(info)
        
    print()
    print("==================================各省情况==================================")
    print()
    hubei_number = soup.findAll("div", class_="expand___wz_07") # hubei_number
    hubei_confirmed = getConfirmedNumer(hubei_number)
    hubei_dead = getDeadNumer(hubei_number)
    hubei_cure = getCureNumber(hubei_number)
    table.add_row(['湖北', hubei_confirmed, hubei_dead, hubei_cure])
    
    
    list_other_area = []
    list_other_confirmed = []
    list_other_dead = []
    list_other_cure= []
    idx = 0
    other_number = soup.findAll('div', class_='fold___xVOZX') # other_number
    for other in other_number:
        list_other_area.append(getArea(other))
        list_other_confirmed.append(getConfirmedNumer(other))
        list_other_dead.append(getDeadNumer(other))
        list_other_cure.append(getCureNumber(other))
        table.add_row([list_other_area[idx], list_other_confirmed[idx], list_other_dead[idx], list_other_cure[idx]])
        idx = idx + 1
    print(table)
    print()
    
    
    idx = 0
    print("==================================最新消息==================================")
    print()

    while True:
        r = requests.get("https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia")
        json_str = json.loads(r.text)
        if json_str['error'] == 0:
            break
    
        
    idx = 0
    for news in json_str['data']['timeline']:
        if idx == 5:
            break
        print(news['pubDateStr'] + "  " + news['title'])
        idx = idx + 1
    
    r = requests.get("https://3g.dxy.cn/newh5/view/pneumonia")
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text,'lxml')
    provinces = soup.findAll("div", "fold___xVOZX")
    idx = 1
    for province in provinces:
        for city in province.children:
            name, confirmed, dead, cure = clear(city)
            for i in range(len(name)):
                provinces_idx[idx][name[i]] = [confirmed[i], dead[i], cure[i]]
        idx = idx + 1

    initMap(soup)

    hubei = soup.findAll("div", "expand___wz_07")
    name, confirmed, dead, cure = clear(hubei)
    for i in range(len(name)):
        provinces_idx[0][name[i]] = [confirmed[i], dead[i], cure[i]]
            

    print()
    key = input("请输入您想查询详细信息的省份，例如 湖北\n")
    print()
    if key in map.keys():
        query(provinces_idx[map[key]])
    else:
        print("暂无相关信息")
        
    print("\n欢迎提出各种意见")
#     except:
#         print("连接失败")

if __name__ == '__main__':
    main()
    sleep(30)
