test_dict = {

}
test_dict["中直机关2018年4季度批量集中采购项目招标公告2018年08月29日 11:29 来源：中国政府采购网 【打印】"] = "123"

# print(test_dict)
import requests
from bs4 import BeautifulSoup


res = requests.get("http://www.ccgp.gov.cn/cggg/dfgg/xjgg/201903/t20190307_11724686.htm")
res.encoding = res.apparent_encoding

soup = BeautifulSoup(res.text,"html.parser")


# count = 0
# list = []

# l = list[1]
trs = soup.select(".vF_detail_content")
for tr in trs:
    print(type(tr.text))
    # tds = tr.select("td")
    # for td in tds:
    #     print(td.text)
    # print("-----------------------")