from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import requests
import wget
import os
import pandas as pd
from bs4 import BeautifulSoup
browser=webdriver.Chrome()
browser.get("https://fr.global.nba.com/statistics/teamstats/")
time.sleep(5)
""" accept cookies """
link = browser.find_element_by_css_selector("#onetrust-accept-btn-handler")
link.click()
time.sleep(2)
"""get all the information on all teams"""
rows = []

for i in range(30):
    rows.append(browser.find_element_by_css_selector('#main-container > div > div.col-xl-8.col-lg-12.content-container > div.content > div > div > div > div:nth-child(2) > div.ng-scope > nba-stat-table > div > div.nba-stat-table__overflow > table > tbody > tr:nth-child('+str(i+1)+')'))

columns = ["Rank","Team","M","FG%","3P%","%LF","REBO","REBD","PPM","RPM","PDPM","BP","IPM","CPM","FP"]
lines = [str(row.text).split(' ') for row in rows]
print(lines)

for i,line in enumerate(lines):
    name = line[1:-13]
    print(name)
    del lines[i][1:-13]
    full_name=""
    for j in range(len(name)):
        full_name +=name[j]
        if j+1!=len(name):
            full_name+=" "
    lines[i].insert(1,full_name)
    print(lines[i])
    print(len(lines[i]))
    #print(len(lines[i]))
print(lines)
    

    
df=pd.DataFrame(lines, columns=columns)
df.index=df['Rank']
df.drop("Rank",axis=1,inplace=True)
df.to_excel('Teams.xlsx')




