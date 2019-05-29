# coding: utf-8

import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup

__auther__ = "Wei"
__date__ = "2019-05-06"
__mail__ = "hanwei@shanghaitech.edu.cn"

baseurl = "https://www.ebi.ac.uk/interpro/entry/IPR000725/proteins-matched"

#First, I will get the number of sequence
res = requests.get(baseurl)
soup = BeautifulSoup(res.text)
divs = soup.find_all(name="span", class_="menu_numb")
seq_num = int(divs[0].string[1:-1])

#second, download information what we need
num, seqinfo = 0, pd.DataFrame()
while num <= seq_num:
	url = baseurl+ "?start=" + str(num)
	res = requests.get(url)
	res_elements = etree.HTML(res.text)
	table = res_elements.xpath('//table[@class="result stripe fluid"]')
	table = etree.tostring(table[0], ecoding='utf-8').decode()
	page_list = pd.read_html(table, encoding='utf-8', header=0)
	assert len(page_list)==1, "This page more than one table"
	seqinfo = seqinfo.append(page_list[0], ignore_index=True)
	num += 20
	print("%d/%d sequences information DONE" % (num, seq_num))

#Now, Save the data
seqinfo.to_excel("IPR000725_info.xlsx", header=True)
