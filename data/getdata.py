import requests
import json
from lxml import etree

rootUrl="http://www.kuaiyilicai.com/stats/global/yearly/g_gdp_per_capita/%d.html"
data=[]

for year in range(1960, 2017+1):
    url=rootUrl%(year)
    html=requests.get(url)
    print(url, ' -> ', html.status_code)

    tree=etree.HTML(html.content)
    for tr in tree.xpath('//tbody/tr'):
        td=tr.xpath('.//td')
        if len(td)<3:
            continue
        value=td[2].xpath('./text()')[0]
        if '万' in value:
            value=value.replace(',', '').replace('(', ')').split(')')[1]
        elem={"name": td[0].xpath('./text()')[0],
                "value": value,
                "date": year}
        data.append(elem)

file=open("data.json", "w", encoding="utf-8")
print(data)
file.write(json.dumps(data))
file.close()
