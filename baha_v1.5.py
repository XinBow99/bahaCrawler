import time as t
import random as rand
from datetime import datetime
from logging import error
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import requests
import re
import json
import time
import exportToExcel
import downloadImage
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", bs4])

from bs4 import BeautifulSoup as bs
from bs4.element import ResultSet,Tag


# initialize the Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())
#driver.maximize_window()
# head to github login page
word = "培根"#搜尋字詞
url = "https://forum.gamer.com.tw/B.php?bsn=60076&qt=1&q=" + word #搜尋網址




class bahaInfo:
    def __init__(self):
        self.funcname = ''
        self.nowTitle = ''
        self.word = ''
        self.mainUrl = "https://forum.gamer.com.tw/"
        self.parser = 'html.parser'
        self.keyWordList = ['培根'] #搜尋字詞的資料夾名稱 可改可不改 我是懶得改
        self.bsn = "60076"
        self.download = T#True的話會下載圖片
        self.pageDelay = 1#一頁停1秒
        self.innerDelay = 1#文章內每頁停1秒

    def search(self):
        #搜尋
        self.funcname = "search"
        for word in self.keyWordList:
            self.word = word
            print('[INFO]搜尋{}'.format(word))
            driver.get(url)            
            print('[INFO]「{}」搜尋成功，進入分析'.format(word))
            self.analysis(driver.page_source)
               

    def analysis(self, data):
        #分析頁數
        self.funcname = "analysis"
        bahaContent = bs(data, self.parser)
        pageInfo = bahaContent.find('p', class_="BH-pagebtnA")

        self.limitPage = bs(
            str(pageInfo), 'html.parser').find_all('a')[-1].text

        self.analysisPages()

    def analysisPages(self):
        self.funcname = "analysisPages"
        maxPage = self.limitPage
        keyWord = self.word
        print("[INFO]共有{}頁".format(maxPage))
        self.page_items = []
        for page in range(1, int(maxPage) + 1):
            driver.get(url)         
            print('[INFO]正在分析第{}頁'.format(page))
            thisContent = bs(driver.page_source, self.parser)
            thisItem = thisContent.find_all('tr', class_="b-imglist-item")
            #print(thisItem)
            self.singlePage(thisItem)
        self.export()
        

    def singlePage(self, data):
        self.funcname = 'singlePage'
        for i,item in enumerate(data):
            summary = str(bs(str(item), self.parser).find('td' ,class_="b-list__summary"))
            #text
            subbsn = self.checkNone(bs(summary, self.parser).find('p' ,class_="b-list__summary__sort"))
            gp = self.checkNone(bs(summary, self.parser).select("span.b-list__summary__gp.b-gp"))

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

            eTime = str(bs(str(item), self.parser).find('td', class_="b-list__time"))
            edittime = str(bs(eTime, self.parser).find('p', class_="b-list__time__edittime"))
            forFloorAndEditTime = bs(edittime, self.parser).find('a')
            tnum = self.checkNone(re.findall(r'tnum=(.*?)&',forFloorAndEditTime['href'])[0])
            sna = self.checkNone(re.findall(r'snA=(.*?)&',forFloorAndEditTime['href'])[0])
            euser = self.checkNone(bs(eTime, self.parser).find('p', class_="b-list__time__user"))
            etime = self.checkNone(forFloorAndEditTime)
                
            this_item = {
                'subbsn':subbsn,
                'snA':sna,
                'best':best,
                'title':title,
                'text':text,
                'gp':int(gp),
                'totalReplyCount':int(number[0].replace('k','000')),
                'engagement':int(number[1].replace('k','000')),
                'user':user,
                'totalFloor':int(tnum.replace('k','000')),
                'lastUser':euser,
                'lastReplyTime':etime
            }
            self.nowTitle = title
            print('[INFO]分析進度{}%'.format(int((i + 1)/len(data) * 100)))
            self.page_items.append(this_item)
            self.singleItem(title, forFloorAndEditTime['href'])
            print("[INFO]請等待{}秒...".format(self.pageDelay))
            time.sleep(self.pageDelay)
            
                
    def singleItem(self, title, url):
        self.funcname = "singleItem"
        print("[INFO]分析「{}」回應".format(title))
        sectionsItems = []
        newUrl = url.replace('&last=1','')
        #https://forum.gamer.com.tw/C.php?bsn=60076&snA=4749438&tnum=3986 self.mainUrl + newUrl
        print(self.mainUrl + newUrl)
        driver.get(self.mainUrl + newUrl) 
        master = str(bs(str(driver.page_source), self.parser).find('div' ,id="BH-master"))
        pageBtn = self.checkNone(bs(master, self.parser).select("p.BH-pagebtnA"),False)
        pageNum = self.checkNone(bs(str(pageBtn), self.parser).select('a'),getDatalen = -1)
        print("[INFO]「{}」共有{}頁".format(title,pageNum))
        pictures = []
        for page in range(1,int(pageNum) + 1):
            print("[INFO]「{}」的第{}頁".format(title,page))
            #result = requests.get(self.mainUrl + newUrl + "&page={}".format(page))
            driver.get(self.mainUrl + newUrl + "&page={}".format(page)) 
            master = str(bs(str(driver.page_source), self.parser).find('div' ,id="BH-master"))
            sections = bs(master, self.parser).find_all('section' ,id=re.compile(r"post_[0-9]+"))
            for section in sections:
                side = str(bs(str(section), self.parser).find('div' ,class_="c-section__side"))
                userSide = str(bs(side, self.parser).find('div' ,class_="c-user__side"))
                #------------Post------------
                postId = self.checkNone(section['id'].replace('post_',''))
                
                #------------user------------
                userLv = self.checkNone(bs(userSide, self.parser).select("div.usericon.userlevel")).replace("LV.","")
                #print(self.checkNone(bs(userSide, self.parser).select("div.usericon.userlevel")))
                #print(type(self.checkNone(bs(userSide, self.parser).select("div.usericon.userlevel"))))
                
                userGp = self.checkNone(bs(userSide, self.parser).select("div.usericon.usergp"))
                #print(self.checkNone(bs(userSide, self.parser).select("div.usericon.usergp"),False,'title'))
                #print(type(self.checkNone(bs(userSide, self.parser).select("div.usericon.usergp"),False,'title')))
                #usercareer = self.checkNone(bs(userSide, self.parser).select("div.usericon.usercareer"))
                #userrace = self.checkNone(bs(userSide, self.parser).select("div.usericon.userrace"))

                userhonor = bs(side, self.parser).find('div' ,class_="c-user__honor")
                #text
                userId = self.checkNone(userhonor, False, 'data-userid', False)['data-userid']

                post = str(bs(str(section), self.parser).find('div' ,class_="c-section__main"))
                header = str(bs(post, self.parser).find('div' ,class_="c-post__header"))
                body = str(bs(post, self.parser).find('div' ,class_="c-post__body"))
                #------------header------------
                #text
                floor = self.checkNone(bs(header, self.parser).select("a.floor"),False,'data-floor')['data-floor']
                postip = self.checkNone(bs(header, self.parser).select("a.edittime.tippy-post-info"),False,'data-hideip')['data-hideip']
                postTime = self.checkNone(bs(header, self.parser).select("a.edittime.tippy-post-info"),False,'data-mtime')['data-mtime']
                #GP
                gp = self.checkNone(bs(header, self.parser).select("span.postgp"),True)
                gpNum = self.checkNone(re.findall(r'([0-9]+|-|爆|X|x)',gp)).replace('-','0')
                #BP
                bp = self.checkNone(bs(header, self.parser).select("span.postbp"),True)
                bpNum = self.checkNone(re.findall(r'([0-9]+|-|爆|X|x)',bp)).replace('-','0')
                if gpNum == 0 and bpNum == 0:
                    continue
                #------------body------------
                mainContent = bs(body, self.parser).select("div.c-article__content")
                content = self.checkNone(mainContent, True)
                picturesLinks = bs(str(self.checkNone(mainContent, False)), self.parser).select("a.photoswipe-image")
                this_picture = []
                if picturesLinks:
                    for picture in picturesLinks:
                        if picture["href"]:
                            this_picture.append(picture["href"])
                    pictures += this_picture
                #------------footer------------
                #comments = self.commentList(postId)

                this_Section = {
                    'postId':postId,
                    'userId':userId,
                    'userLv':userLv,
                    'userGp':userGp,
                    #'usercareer':usercareer,
                    #'userrace':userrace,
                    'userfloor':floor,
                    'postip':postip,
                    'postTime':postTime,
                    'getgp':gpNum,
                    'getbp':bpNum,
                    'content':content,
                    'pictures':this_picture,
                    #'comments':comments
                }
                sectionsItems.append(this_Section)
            time.sleep(self.innerDelay)
        
        self.page_items[-1].update({'postDate':sectionsItems[0]['postTime']})
        self.page_items[-1].update({'totalPicturesNum':len(pictures)})
        self.page_items[-1].update({'totalPictures':pictures})
        self.page_items[-1].update({'contentLen':len(sectionsItems[0]['content'])})
        self.page_items[-1].update({'detail':sectionsItems})
        if len(pictures)>0 and self.download:
            downloadImage.download(title,self.page_items[-1]['snA'],pictures,self.word)
    '''
    def commentList(self, id):
        self.funcname = 'commentList'
        result = str(requests.get('{}/ajax/moreComment.php?bsn={}&snB={}&returnHtml=0'.format(self.mainUrl, self.bsn, id)).text)
        result = json.loads(result)
        return result       
    '''
    def export(self):
        self.funcname = 'export'
        data = self.page_items
        exportToExcel.showD2T(data)
        exportToExcel.export2Excel(data, self.word)

    def checkNone(self, data, formatThis = True, dictFormat='',TagText = True,getDatalen = 0):
        self.funcname = 'checknone'
        if data:
            if type(data) == str:
                data = data
            elif  type(data) == int:
                data = data
            elif  type(data) == list:
                data = data[getDatalen]
            elif  type(data) == Tag:
                if TagText:
                    data = data.text.replace('\n','').replace('&#xE838;','')
                else:
                    data = data
            elif  type(data) == ResultSet:
                if formatThis:
                    data = data[getDatalen].text.replace('\n','')
                else:
                    data = data[getDatalen]
            else:
                data = data.text.replace('\n','').replace('&#xE838;','')
        else:
            if  type(data) == ResultSet:
                if dictFormat != '':
                    data = {dictFormat:'0'}
                else:
                    data = '0'
            elif  type(data) == Tag:
                if dictFormat != '':
                    data = {dictFormat:'0'}
                else:
                    data = '0'
            elif  type(data) == list:
                data = '0'
            else:
                data = '0'
        return data

if __name__ == "__main__":
    main = bahaInfo()
    main.search()

    
