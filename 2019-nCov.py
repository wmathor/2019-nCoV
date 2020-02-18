import requests
import re
from random import randint
from bs4 import BeautifulSoup
from time import sleep
import json
from prettytable import ALL
from prettytable import PrettyTable

                     #  省份           城市,  确诊, 死亡,  治愈, 疑似
# China = [{"province":"河南", cities:[[信阳", 10,   0,    10,   10], [], []]}, {}, {}, {}]
China = []
headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
        'accept':'*/*',
        'Connection':'keep-alive',
        'Referer':'https://lab.isaaclin.cn/nCoV/',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Upgrade-Insecure-Requests':'1'

    }

def query(province):
    table = PrettyTable(['地区', '确诊', '死亡', '治愈'])
    url = "https://lab.isaaclin.cn/nCoV/api/area?latest=1&province=" + province
    json_str = json.loads(requests.get(url, headers=headers).text)
    if json_str['success']:
        if len(json_str['results'][0]['cities']):
            for data in json_str['results'][0]['cities']:
                confirmed = data['confirmedCount'] if data['confirmedCount'] != 0 else '-'
                dead = data['deadCount'] if data['deadCount'] != 0 else '-'
                cured = data['curedCount'] if data['curedCount'] != 0 else '-'
                table.add_row([data['cityName'], confirmed, dead, cured])
            print(table)
            return
        else:
            print("暂无相关信息")
    else:
        print("暂无相关信息")
        return

def is_json(json_str):
    try:
        json.loads(json_str)
    except ValueError:
        return False
    return True      

def main():
    try:

        url = "https://lab.isaaclin.cn/nCoV/api/overall"
        table = PrettyTable(['地区', '确诊', '死亡', '治愈'])
        table.hrules = ALL

        while True:
            r = requests.get(url, headers=headers)
            r.encoding = r.apparent_encoding
            json_str = json.loads(r.text)
            if json_str['success']:
                break
            else:
                sleep(1)

        print()
        print("==================================全国数据==================================")
        print()
        
        print("  确诊 " + str(json_str['results'][0]['confirmedCount']) + " 例"
            + "       " + "疑似 " + str(json_str['results'][0]['suspectedCount']) + " 例"
            + "       " + "死亡 " + str(json_str['results'][0]['deadCount']) + " 例"
            + "       " + "治愈 " + str(json_str['results'][0]['curedCount']) + " 例\n")

        print("==================================相关情况==================================")
        print()
        
        print(json_str['results'][0]['remark3'])
        print(json_str['results'][0]['note1'])
        print(json_str['results'][0]['note2'])
        print(json_str['results'][0]['remark1'])
        print(json_str['results'][0]['note3'])
        print(json_str['results'][0]['remark2'] + "\n")
            
        print("==================================国内情况==================================")
        print()

        url = "http://www.dzyong.top:3005/yiqing/province"

        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        json_info = json.loads(r.text)
        
        for data in json_info['data']:
            confirmed = data['confirmedNum'] if data['confirmedNum'] != 0 else '-'
            dead = data['deathsNum'] if data['deathsNum'] != 0 else '-'
            cured = data['curesNum'] if data['curesNum'] != 0 else '-'
            table.add_row([data['provinceName'], confirmed, dead, cured])
        
        print(table)

        
        
        print()
        print("==================================国外情况==================================")
        print()

        url = "https://lab.isaaclin.cn/nCoV/api/area"
        table = PrettyTable(['地区', '确诊', '死亡', '治愈'])
        table.hrules = ALL

        while True:
            r = requests.get(url, headers=headers)
            r.encoding = r.apparent_encoding
            json_str = json.loads(r.text)
            if json_str['success']:
                break
            else:
                sleep(1)

        for data in json_str['results']:
            if data['countryName'] != '中国' and data['countryName'] != "“钻石公主”号邮轮" and data['countryName'] != "邮轮":
                confirmed = data['confirmedCount'] if data['confirmedCount'] != 0 else '-'
                dead = data['deadCount'] if data['deadCount'] != 0 else '-'
                cured = data['curedCount'] if data['curedCount'] != 0 else '-'
                table.add_row([data['provinceName'], confirmed , dead, cured])
        
        print(table)
        print()
        
        


        print("==================================最新消息==================================")
        print()

        url = "https://lab.isaaclin.cn/nCoV/api/news"
        while True:
            json_info = json.loads(requests.get(url, headers=headers).text)
            if json_info['success']:
                break
            else:
                sleep(1)

        idx = 0
        for data in json_info['results']:
            if idx >= 5:
                break
            print(str(data['title']).strip())
            idx = idx + 1
        

        print()
        key = input("请输入您想查询详细信息的省份，例如 湖北省 或 香港\n")
        print()
        query(key)
            
        print("\n欢迎提出各种意见")
    except:
        print("连接失败，请在Github中提出Issue，或者联系QQ16036505")

if __name__ == '__main__':
    main()
    sleep(30)