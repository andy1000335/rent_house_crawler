from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import os

path = os.path.abspath('.')    #取得目前的工作目錄

driver = webdriver.Chrome()    #開啟瀏覽器(Chrome)
driver.get('https://rent.591.com.tw')    #前往指定的網址

chooseCountry = []
chooseArea = []

findChooseCountries = driver.find_elements_by_xpath("//dl[@class='clearfix']")
for findChooseCountry in findChooseCountries:
    countries = findChooseCountry.find_elements_by_tag_name('dd')
    for country in countries:
        chooseCountry.append(country)

del chooseCountry[0:4]    #list前4個不是所需要的


print('北部：   1.台北市   2.新北市   3.桃園市   4.新竹市   5.新竹縣   6.宜蘭縣   7.基隆市')
print('中部：   8.台中市   9.彰化縣  10.雲林縣  11.苗栗縣  12.南投縣')
print('南部：  13.高雄市  14.台南市  15.嘉義市  16.嘉義縣  17.屏東縣')
print('東部：  18.台東縣  19.花蓮縣  20.澎湖縣  21.金門縣  22.連江縣')

countryIndex = int(input('請選擇縣市：'))    #選擇縣市
while countryIndex<=0 or countryIndex>22:
    countryIndex = int(input('輸入錯誤，請重新輸入：'))


countryIndex -= 1
action = ActionChains(driver)
action.click(chooseCountry[countryIndex]).perform()   #滑鼠點擊所選之縣市
time.sleep(5)    #延遲5秒

action = ActionChains(driver)
serchLocation = driver.find_element_by_class_name('select')
action.click(serchLocation)
action.click(serchLocation).perform()


areas = driver.find_elements_by_class_name("rion")
for area in areas:
    chooseArea.append(area)

html = driver.execute_script('return document.documentElement.outerHTML')    #取得html
soup = BeautifulSoup(html,'html.parser')    #解析html
printAreas = soup.findAll('li', 'rion')

areasList = []
i = 0
for printArea in printAreas:
    areasList.append(printArea.find('span').text)
for printArea in areasList:    #顯示所選縣市之所有地區
    space = ''
    i += 1
    if i<10:
        space = ' '    #數字若為個位數則在前面加一個空格
    if i%10==1:
        print()
    if len(printArea)==2:
        printArea += '  '    #地區名若只有兩個字則在後面加兩個空格
    print('{0}{1}.{2}'.format(space, i, printArea), end='  ')

print()
areaIndex = int(input('請選擇地區：'))    #選擇地區
while areaIndex<=0 or areaIndex>i:
    areaIndex = int(input('輸入錯誤，請重新輸入：'))
areaIndex -= 1

action = ActionChains(driver)
action.click(chooseArea[areaIndex]).perform()

time.sleep(3)    #延遲3秒

html = driver.execute_script('return document.documentElement.outerHTML')    #取得html
driver.close()    #關閉瀏覽器
soup = BeautifulSoup(html,'html.parser')    #解析html

getDatas = soup.findAll('ul', 'listInfo')

with open(path + r'\crawler.txt', 'r+') as f:
    f.truncate()    #清空txt檔

titleList = []
linkList = []
detailList = []
placeList = []
priceList = []
compareList = []
i = 0

for getData in getDatas:
    infoContent = getData.find('li', 'infoContent')

    getTitle = infoContent.find('a').text.replace(' ', '').replace('\n', '')
    titleList.append(getTitle)    #將標題存於list

    getLink = infoContent.find('a').get('href')
    linkList.append(getLink)    #將網址存於list

    getDetail = infoContent.find('p', 'lightBox').text.replace('|', '').replace(' ', '').replace('\n', '')
    detailList.append(getDetail)    #將資訊存於list

    getPlace = infoContent.find('em').text
    placeList.append(getPlace)    #將地址存於list

    getPrice = getData.find('div', 'price').text.replace('\n', '').replace(' ', '').replace('元/月', '')
    getPrice += ' 元/月'
    priceList.append(getPrice)    #將價格存於list

    price = int(getPrice.replace(',', '').replace('元/月', ''))    #將價錢轉為int
    compareList.append(price)    #用於比價
    
    i += 1

if len(titleList)==0:
    with open(path + r'\crawler.txt', 'a', encoding='UTF-8') as f:
        f.write('此地區目前無任何資料')
    print('\n此地區目前無任何資料')
else:
    sort = input('是否要按照價格排序(Y/N)：')
    while not(sort=='Y' or sort=='y' or sort=='N' or sort=='n'):
        sort = input('輸入錯誤，請重新輸入(Y/N)：')
    if sort=='N' or sort=='n':
        for j in range(i):    #共i+1筆資料
            with open(path + r'\crawler.txt', 'a', encoding='UTF-8') as f:
                f.write('{0}\nhttps:{1}\n{2}\n{3}\n{4}\n\n'.format(titleList[j], linkList[j], detailList[j], placeList[j], priceList[j]))    #寫入txt檔

    if sort=='Y' or sort=='y':
        for j in range(i):    #共i+1筆資料
            a = compareList.index(min(compareList))    #找出價格最低的位於list的哪個位置
            compareList[a] = 999999999    #將此價格設為最大避免重複
            with open(path + r'\crawler.txt', 'a', encoding='UTF-8') as f:
                f.write('{0}\nhttps:{1}\n{2}\n{3}\n{4}\n\n'.format(titleList[a], linkList[a], detailList[a], placeList[a], priceList[a]))    #寫入txt檔

    print('\n資料抓取成功，請開啟crawler.txt觀看結果')