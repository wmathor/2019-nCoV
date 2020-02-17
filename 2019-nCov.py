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


def query(province):
    table = PrettyTable(['地区', '确诊', '死亡', '治愈'])

    for (k, v) in province.items():
        name = k
        table.add_row([name, v[0] if v[0] != 0 else '-', v[1] if v[1] != 0 else '-', v[2] if v[2] != 0 else '-'])
    if len(province.keys()) != 0:
        print(table)
    else:
        print("暂无")

def is_json(json_str):
    try:
        json.loads(json_str)
    except ValueError:
        return False
    return True

        

def main():
    url = "https://tianqiapi.com/api?version=epidemic&appid=98687232&appsecret=1GGIGivo"
    try:
        headers = {}
        headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36' #http头大小写不敏感
        headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        headers['Connection'] = 'keep-alive'
        headers['Upgrade-Insecure-Requests'] = '1'

        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        table = PrettyTable(['地区', '确诊', '死亡', '治愈'])
        table.hrules = ALL

        while True:
            r = requests.get(url)
            json_str = json.loads(r.text)
            if json_str['errcode'] == 0:
                break

        print()
        print("==================================全国数据==================================")
        print()
        
        print("   确诊 " + str(json_str['data']['diagnosed']) + " 例"
            + "       " + "疑似 " + str(json_str['data']['suspect']) + " 例"
            + "       " + "死亡 " + str(json_str['data']['death']) + " 例"
            + "       " + "治愈 " + str(json_str['data']['cured']) + " 例\n")

        url_info = "https://lab.isaaclin.cn/nCoV/api/overall"
        while True:
            json_info = json.loads(requests.get(url_info, headers=headers).text)
            if json_info['success']:
                break

        print("==================================相关情况==================================")
        print()
        
        print(json_info['results'][0]['note1'])
        print(json_info['results'][0]['remark3'])
        print(json_info['results'][0]['note2'])
        print(json_info['results'][0]['remark1'])
        print(json_info['results'][0]['note3'])
        print(json_info['results'][0]['remark2'] + "\n")
            
        print("==================================国内情况==================================")
        print()
        
        json_provinces = json_str['data']['area']
        idx = 0
        for province in json_provinces:
            province_name = province['provinceShortName']
            confirmed = province['confirmedCount'] if province['confirmedCount'] != 0 else '-'
            cured = province['curedCount'] if province['curedCount'] != 0 else '-'
            dead = province['deadCount'] if province['deadCount'] != 0 else '-'
            table.add_row([province_name, confirmed, dead, cured])
            map[province_name] = idx
            idx = idx + 1
            for city in province['cities']:
                provinces_idx[map[province_name]][city['cityName']] = [city['confirmedCount'], city['deadCount'], city['curedCount']]

        print(table)
        
        
        print()
        # print("==================================国外情况==================================")
        # print()

        # table = PrettyTable(['地区', '确诊', '死亡', '治愈'])
        # for other in json_str['data']['listByOther']:
        #     table.add_row([other['name'], other['confirmed'], other['dead'], other['cured']])
        
        # print(table)
        # print()
        
        url_info = "https://lab.isaaclin.cn/nCoV/api/news"
        while True:
            if is_json(requests.get(url_info).text):
                json_info = json.loads(requests.get(url_info).text)
                if json_info['success']:
                    break

        print("==================================最新消息==================================")
        print()
        
        for i in range(5):
            print(json_info["results"][i]['title'])
        

        print()
        key = input("请输入您想查询详细信息的省份，例如 湖北\n")
        print()
        if key in map.keys():
            query(provinces_idx[map[key]])
        else:
            print("暂无相关信息")
            
        print("\n欢迎提出各种意见")
    except:
        print("连接失败，请在Github中提出Issue，或者联系QQ16036505")

if __name__ == '__main__':
    main()
    sleep(30)