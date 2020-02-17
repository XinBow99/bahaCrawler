import requests
import re
import exportToExcel
from bs4 import BeautifulSoup as bs


class bahaInfo:
    def __init__(self):
        self.keyWordList = ['宵夜']
        self.word = ""
        self.parser = 'html.parser'

    def search(self):
        """搜尋"""
        for word in self.keyWordList:
            self.word = word
            print('[INFO]搜尋{}'.format(word))
            result = requests.get(
                'https://forum.gamer.com.tw/B.php?bsn=60076&qt=1&q={}'.format(word))
            if result.status_code == 200:
                print('[INFO]「{}」搜尋成功，進入分析'.format(word))
                self.analysis(result.text)

    def analysis(self, data):
        """分析頁數"""
        bahaContent = bs(data, self.parser)
        pageInfo = bahaContent.find('p', class_="BH-pagebtnA")

        self.limitPage = bs(
            str(pageInfo), 'html.parser').find_all('a')[-1].text

        self.analysisPages()

    def analysisPages(self):
        maxPage = self.limitPage
        keyWord = self.word
        print("[INFO]共有{}頁".format(maxPage))
        self.page_items = []
        for page in range(1, int(maxPage) + 1):
            result = requests.get(
                'https://forum.gamer.com.tw/B.php?page={}&bsn=60076&qt=1&q={}'.format(page, keyWord))
            if result.status_code == 200:
                print('[INFO]正在分析第{}頁'.format(page))
                thisContent = bs(result.text, self.parser)
                thisItem = thisContent.find_all('tr', class_="b-imglist-item")
                self.singlePage(thisItem)
        self.export()
        

    def singlePage(self, data):
        for item in data:
            summary = str(bs(str(item), self.parser).find('td' ,class_="b-list__summary"))
            #text
            subbsn = self.checkNone(bs(summary, self.parser).find('p' ,class_="b-list__summary__sort"))
            gp = self.checkNone(bs(summary, self.parser).find('span', class_="b-gp--normal"))
            
            main = str(bs(str(item), self.parser).find('td', class_="b-list__main"))
            imglist = str(bs(main, self.parser).find('div', class_="imglist-text"))
            #text
            best = self.checkNone(bs(imglist, self.parser).find(attrs={"title":"精華"}))
            title = self.checkNone(bs(imglist, self.parser).find('p', class_="b-list__main__title"))
            text = self.checkNone(bs(imglist, self.parser).find('p', class_="b-list__brief"))

            count = str(bs(str(item), self.parser).find('td', class_="b-list__count"))
            #text
            number = self.checkNone(bs(count, self.parser).find('p', class_="b-list__count__number")).split('/')
            user = self.checkNone(bs(count, self.parser).find('p', class_="b-list__count__user"))
            try:
                eTime = str(bs(str(item), self.parser).find('td', class_="b-list__time"))
                edittime = str(bs(eTime, self.parser).find('p', class_="b-list__time__edittime"))
                forFloorAndEditTime = bs(edittime, self.parser).find('a')
                tnum = self.checkNone(re.findall(r'&tnum=(.*?)&',forFloorAndEditTime['href'])[0])
                euser = self.checkNone(bs(eTime, self.parser).find('p', class_="b-list__time__user"))
                etime = self.checkNone(forFloorAndEditTime)

                this_item = {
                    'subbsn':subbsn,
                    'gp':int(gp.replace('k','000')),
                    'best':best,
                    'title':title,
                    'text':text,
                    'totalReplyCount':int(number[0].replace('k','000')),
                    'engagement':int(number[1].replace('k','000')),
                    'user':user,
                    'floor':int(tnum.replace('k','000')),
                    'lastUser':euser,
                    'lastReplyTime':etime
                }
                self.page_items.append(this_item)
            except:
                print("[ERROR]{}出現了錯誤".format(title))
                
    def export(self):
        data = self.page_items
        exportToExcel.showD2T(data)
        exportToExcel.export2Excel(data, self.word)

    def checkNone(self, data):
        if data:
            if type(data) == str:
                data = data
            else:
                data = data.text.replace('\n','').replace('&#xE838;','')
        else:
            data = '0'
        return data

if __name__ == "__main__":
    main = bahaInfo()
    main.search()
