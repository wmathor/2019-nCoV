import os
import json
import requests
import datetime
import warnings
import schedule
from time import sleep
from openpyxl import load_workbook, Workbook
warnings.filterwarnings('ignore')


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

def getData():
    url = "https://tianqiapi.com/api?version=epidemic&appid=98687232&appsecret=1GGIGivo"
    headers = {}
    headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36' #http头大小写不敏感
    headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'

    while True:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        json_str = json.loads(r.text)
        if json_str['errcode'] == 0:
            break
    idx = 0
    for data in json_str['data']['area']:
        if data['provinceShortName'] == '待确认地区':
            break
        map[data['provinceShortName']] = idx
        provinces_idx[idx]['name'] = data['provinceShortName']
        provinces_idx[idx]['confirmed'] = data['confirmedCount']
        provinces_idx[idx]['dead'] = data['deadCount']
        provinces_idx[idx]['cured'] = data['curedCount']
        provinces_idx[idx]['suspected'] = data['suspectedCount']
        provinces_idx[idx]['cities'] = []
        
        for city in data['cities']:
            if city['cityName'] == '待确认地区':
                break
            tmp = {}
            tmp['name'] = city['cityName']
            tmp['confirmed'] = city['confirmedCount']
            tmp['dead'] = city['deadCount']
            tmp['cured'] = city['curedCount']
            tmp['suspected'] = city['suspectedCount']
            provinces_idx[idx]['cities'].append(tmp)
        idx = idx + 1

def data_to_excel(my_sheet, cur_day):
    row = ['省份', '城市', '日期', '确诊', '死亡', '治愈', '疑似']
    my_sheet.append(row)

    for i in range(34):
        province = provinces_idx[i]['name']
        if len(provinces_idx[i]['cities']) != 0:
            for city in provinces_idx[i]['cities']:
                tmp = []
                tmp = [province, city['name'], cur_day, city['confirmed'], city['dead'], city['cured'], city['suspected']]
                my_sheet.append(tmp)
        else:
            tmp = []
            tmp = [province, '', cur_day, provinces_idx[i]['confirmed'], provinces_idx[i]['dead'], provinces_idx[i]['cured'], provinces_idx[i]['suspected']]
            my_sheet.append(tmp)

def main():

    cur_day = datetime.date.today().strftime('%m-%d')
    try:
        getData()
    except:
        print("接口出错")

    fname = "2019-nCoV.xlsx"

    try:
        if os.path.exists(fname):
            wb = load_workbook(fname)
        else:
            wb = Workbook()
        my_sheet = wb.create_sheet(cur_day)
    except:
        print("文件路径有问题，请检查是否打开了文件，如果打开了，请关闭")
    
    try:
        data_to_excel(my_sheet, cur_day)
        cur_day = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(cur_day + " 文件写入成功")
    except:
        print("文件写入过程中出现问题")
    finally:
        wb.save(fname)


if __name__ == '__main__':
    schedule.every().day.at("00:00").do(main)
    while True:
        schedule.run_pending()
        sleep(10)