import requests
html = requests.get("http://210.38.64.104/xscj_gc.aspx?xh=15551102054&xm=%C2%ED%D4%F3%BB%AA&gnmkdm=N121613").text
print(html)