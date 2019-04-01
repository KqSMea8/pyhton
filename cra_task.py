from bs4 import BeautifulSoup
import requests,random,threadpool
import Drivers as Drivers
import pandas as pd
from pymongo import MongoClient
import os,time

with open(os.path.abspath('.') + '/user_agent.txt', 'r') as u:
    user_agents = u.read().split('\n')[0:-1]

client = MongoClient("mongodb://127.0.0.1:27017/?authSource=admin")
db = client["wunderground"]
collection = db["wunderground_content"]

def check_link(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.text)
        return r.text
    except:
        print('failed')

# def get_contents(ulist,rurl):
#     soup = BeautifulSoup(urlopen(rurl),'lxml')
#     for tr in soup.find_all('tr _ngcontent-16'):
#         ulist=[]
#         for td in tr.find_all('td tr _ngcontent-16'):
#             ui = []
#             ui.append(td.string)
#         ulist.append(ui)

def cra_task(url):

    date = url.split("   ")[-1]
    url = url.split("   ")[0]
    dri = Drivers.get_chrome(random.choice(user_agents))
    try:
        dri.get(url)
    except:
        print(date,0)
    dri.implicitly_wait(10)
    for i in range(1, 2):
        for i in range(3):
            dri.execute_script("window.scrollBy(0, document.body.scrollHeight/3)")
            time.sleep(1)
    soup = BeautifulSoup(dri.page_source,"html.parser")
    trs = soup.select('table.tablesaw-sortable > tbody > tr')
    print(date,len(trs))
    for tr in trs:
        data = {}
        tds = tr.select("td")
        data["Time"] = tds[0].text.replace("\n","")
        data["Temperature"] = tds[1].text.replace("\n","")
        data["Dew Point"] = tds[2].text.replace("\n","")
        data["Humidity"] = tds[3].text.replace("\n","")
        data["Wind"] = tds[4].text.replace("\n","")
        data["Wind Speed"] = tds[5].text.replace("\n","")
        data["Wind Gust"] = tds[6].text.replace("\n","")
        data["Pressure"] = tds[7].text.replace("\n","")
        data["Precip"] = tds[8].text.replace("\n","")
        data["Precip Accum"] = tds[9].text.replace("\n","")
        data["Condition"] = tds[10].text.replace("\n","")
        data["Date"] = date
        data["url"] = url
        collection.insert_one(data)

    dri.close()





if __name__ == '__main__':
    # with open(os.path.abspath('.') + '/safe.text', 'r', encoding='utf-8') as u:
    #     user_agents = u.read().split('\n')[0:-1]
    result_list = []
    # for i in user_agents:
    #     url = 'https://www.wunderground.com/history/daily/KBLM/date/' + i.split(" ")[0] + '?req_city=Oakhurst&req_state=NJ&req_statename=New%20Jersey&reqdb.zip=07755&reqdb.magic=1&reqdb.wmo=99999' + "   " + i.split(" ")[0]
    #     result_list.append(url)
    pool = threadpool.ThreadPool(5)

    year='2018'

    flag = True

    for month in range(1, 13):
        month = str(month)
        for day in range(1, 28):
            day = str(day)
            url = 'https://www.wunderground.com/history/daily/KBLM/date/' + year + '-' + month + '-' + day + '?req_city=Oakhurst&req_state=NJ&req_statename=New%20Jersey&reqdb.zip=07755&reqdb.magic=1&reqdb.wmo=99999'
            # print(url)
            # check_link(url)
            # if(year+month+day == "2018511"):
            #     flag = False
            # if(flag):
            #     continue
            result_list.append(url+"   "+year+month+day)
            # print(year+month+day)
            # cra_task(url+"   "+year+month+day)
            # print(url)
    tasks = threadpool.makeRequests(cra_task, result_list)
    [pool.putRequest(task) for task in tasks]
    pool.wait()
