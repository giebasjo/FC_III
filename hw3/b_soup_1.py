# b_soup_1.py -- a test of BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

html = urlopen('https://www.treasury.gov/resource-center'
              '/data-chart-center/interest-rates/Pages/'
              'TextView.aspx?data=yieldYear&year=2018')


df = pd.read_html(html)
print(df.head())
"""
bsyc = BeautifulSoup(html.read(), "xml")

fout = open('bsyc_temp.txt', 'wt', encoding='utf-8')

fout.write(str(bsyc))

fout.close()
"""
'''
# display the first table in bsyc
print(bsyc.table)

all_tables = bsyc.findAll('table')
print('there are', len(all_tables), 'table tags')

for t in all_tables:
    print(str(t)[:50])

tc_table_list = bsyc.findAll('table',
                             { "class" : "t-chart" })
print(len(tc_table_list), 't-chart tables')

tc_table = tc_table_list[0]
for c in tc_table.children:
    print(str(c)[:50])

for c in tc_table.children:
    for r in c.children:
        print(str(r)[:50])

for c in tc_table.children:
    for r in c.children:
        print(r.contents)

'''
