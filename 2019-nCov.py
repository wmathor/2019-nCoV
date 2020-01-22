import requests
import re
import time
from bs4 import BeautifulSoup

def main():
    url = "https://3g.dxy.cn/newh5/view/pneumonia"


    def getTime(text):
        TitleTime = str(text)
        TitleTime = TitleTime.replace("[<p class=\"mapTitle___2QtRg\">", "")
        TitleTime = TitleTime.replace("</p>]", "")
        return TitleTime 

    def getAllCountry(text):
        AllCountry = str(text)
        AllCountry = AllCountry.replace("[<p class=\"confirmedNumber___3WrF5\"><span class=\"content___2hIPS\">", "")
        AllCountry = AllCountry.replace("<span style=\"color: #4169e2\">", "")
        AllCountry = re.sub("</span>", "", AllCountry)
        AllCountry = AllCountry.replace("</p>]", "")
        return AllCountry 

    def clear(text):
        text = re.sub("<p class=\"descList___3iOuI\">", "", text)
        text = re.sub("<i class=\"red___3VJ3X\">", "", text)
        text = re.sub("<span>", "", text)
        text = re.sub("<i class=\"orange___1FP2_\">", "", text)
        text = re.sub("<span style=\"color: #4169e2\">", "", text)
        text = re.sub("</p>", "", text)
        text = re.sub("</span>" ,"", text)
        text = re.sub("</i>", "", text)
        return text

    def getNewsTime(text):
        text = re.sub("<div class=\"tabLeft2___SbuNE\"><span class=\"leftTime___2zf53\">", "", text)
        text = re.sub("<br/>", " ", text)
        text = text.replace("<span style=\"font-size: 10px; color: rgb(153, 153, 153);\">", "")
        text = text.replace("</span></span><span class=\"leftDot___2cvKP\"></span><span class=\"leftLine___31ohl\"></span></div>", "")
        return text + " "

    def getNewsTitle(text):
        text = re.sub("<p class=\"topicTitle___2ovVO\">", "", text)
        text = re.sub("<i>", "", text)
        text = re.sub("</i>", " ", text)
        text = text.replace("</p>", "")
        return text + " "

    try:

        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text,'lxml')

        #### 截至时间
        TitleTime = getTime(soup.select('.mapTitle___2QtRg'))

        print()
        print("                     ",TitleTime)
        print("==================================全国数据==================================")
        AllCountry = getAllCountry(soup.select('.confirmedNumber___3WrF5'))
        print("\n" + AllCountry + "\n")

        print("==================================相关情况==================================")
        number = soup.find_all("p", class_="descList___3iOuI")
        idx = 0

        print()
        for t in number:
            idx = idx + 1
            if idx == 6:
                print()
                print("==================================各省情况==================================")
                print()
            t = clear(str(t))
            print(t)

        print()
        print("查看最新消息请摁1，结束请摁0")
        key = input()
        idx = 0
        if key == "1":
            print("==================================最新消息==================================")
            print()

            news_time = soup.find_all("div", class_="tabLeft2___SbuNE")
            news_title = soup.find_all("p", class_="topicTitle___2ovVO")

            list_news_time = []
            list_news_title = []
            for new_time in news_time:
                idx = idx + 1
                if idx == 4:
                    break;
                list_news_time.append(getNewsTime(str(new_time)))

            idx = 0
            for new_title in news_title:
                idx = idx + 1
                if idx == 4:
                    break;
                list_news_title.append(getNewsTitle(str(new_title)))

            for i in range(idx - 1):
                print(list_news_time[i] + list_news_title[i])
        print("\n欢迎提出各种意见，如发现内容不正确请联系QQ739616037")
    except:
        print("连接失败，请联系管理员检查相关问题QQ739616037")

if __name__ == '__main__':
    main()
    time.sleep(20)