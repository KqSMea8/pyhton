import Drivers as Drivers
from selenium.webdriver.common.action_chains import ActionChains
import os,random,json
import time,io,hashlib,threadpool
from lxml import etree
from pymongo import MongoClient
import requests,re
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select

class Pybin():
    def __init__(self):
        with open(os.path.abspath('.') + '/user_agent.txt', 'r') as u:
            user_agents = u.read().split('\n')[0:-1]

        self.__agents = user_agents

        self.client = MongoClient("mongodb://127.0.0.1:27017/?authSource=admin")
        self.db = self.client["xs"]
        self.collection = self.db["xs_main"]

    def extract_cookies(self,cookie):
        cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
        return cookies

    def cra_bin(self,url):
        dri = Drivers.get_chrome(random.choice(self.__agents))
        dri.get(url)
        dri.find_element_by_css_selector('#casLogin > div > form > div.username > input[type="text"]').send_keys("mazehua")
        time.sleep(1)
        dri.find_element_by_css_selector('#password').send_keys("588mzh627")
        time.sleep(1)
        dri.find_element_by_css_selector('input.btn').click()
        time.sleep(2)
        allHandles = dri.window_handles
        dri.switch_to_window(allHandles[-1])
        # dri.refresh()
        # time.sleep(5)
        iframe1 = dri.find_element_by_css_selector("div.portlet-content-inner > iframe")
        dri.switch_to.frame(iframe1)
        time.sleep(2)

        dri.find_element_by_css_selector('a[href="http://210.38.64.104/login_cas.aspx"]').click()
        time.sleep(5)

        allHandles = dri.window_handles
        dri.switch_to_window(allHandles[-1])
        time.sleep(3)

        point_m = dri.find_element_by_xpath('//*[@id="headDiv"]/ul/li[6]')
        ActionChains(dri).move_to_element(point_m).double_click().perform()
        time.sleep(5)
        dri.find_element_by_xpath('//*[@id="headDiv"]/ul/li[6]/ul/li[6]/a').click()
        time.sleep(1)
        # ok = input("a")
        # iframe2 = dri.find_element_by_css_selector("#iframeautoheight")
        dri.switch_to.frame("iframeautoheight")
        time.sleep(1)
        dri.find_element_by_xpath('//*[@id="Button1"]').click()
        time.sleep(2)

        # dri.switch_to.frame("iframeautoheight")
        print(dri.page_source)
        self.cra_data(dri.page_source)

        # dri.find_element_by_xpath('//ax[@href="http://210.38.64.104/login_cas.aspx"]').click()

        dri.close()
    def cra_data(self,html):
        soup = BeautifulSoup(html, "html.parser")
        trs = soup.select("table.datelist > tbody > tr")

        tds = trs[0].select("td")
        
        for td in tds:
            print(td.text)
        flag = True
        for tr in trs:
            if(flag):
                flag = False
                continue
            tds = tr.select("td")
            data = {}
            data["学年"] = tds[0].text
            data["学期"] = tds[1].text
            data["课程代码"] = tds[2].text
            data["课程名称"] = tds[3].text
            data["课程性质"] = tds[4].text
            data["课程归属"] = tds[5].text
            data["学分"] = tds[6].text
            data["绩点"] = tds[7].text
            data["成绩"] = tds[8].text
            data["辅修标记"] = tds[9].text
            data["补考成绩"] = tds[10].text
            data["重修成绩"] = tds[11].text
            data["学院名称"] = tds[12].text
            data["备注"] = tds[13].text
            data["重修标记"] = tds[14].text
            data["课程英文名称"] = tds[15].text
            # for td in tds:
            #     print(td.text)
            print(data)
            self.collection.insert_one(data)
if __name__ == '__main__':
    cra = Pybin()
    url = "http://www.gdei.edu.cn/"
    cra.cra_bin(url)
