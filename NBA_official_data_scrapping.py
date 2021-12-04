import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import codecs
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests
from pprint import pprint
import pickle

#s  = HTMLSession()
#html = s.get(stats_individuelles_url).html.html
#html = requests.get(stats_individuelles_url).text


def show(html, file='test.html'):
    file = codecs.open(file, "w", "utf-8")
    file.write(html)
    file.close()
    return



def get_columns(driver, selector_dic):
    columns = []
    i = 0
    while True:
        i += 1
        try:
            selector = f"body > main > div > div > div.row > div > div > nba-stat-table > div.nba-stat-table > div.nba-stat-table__overflow > table > thead > tr > th:nth-child({i+1})"
            elem = driver.find_element_by_css_selector(selector)
            a = 1/len(elem.text)    # Astuce bien crado pour break au premier élément nul trouvé
            columns.append(elem.text)
        except:
            break;
    return columns

def get_players_stats(selector_dic):
    ## Get URL using Selenium
    driver = webdriver.Chrome('C:/chromedriver96.exe')
    driver.get(selector_dic['url']) 
    time.sleep(2)

    button = driver.find_element_by_css_selector("#onetrust-accept-btn-handler")
    button.click()
    time.sleep(3)

    #columns = driver.find_element_by_css_selector("body > main > div > div > div.row > div > div > nba-stat-table > div.nba-stat-table > div.nba-stat-table__overflow > table > thead > tr")
    #columns = columns.text
    columns = get_columns(driver, selector_dic)
    
    STATS = []
    DATA = {}
    for p in range(selector_dic['nb pages']):
        for i in range(50):
            try:
                selector = f"body > main > div > div > div.row > div > div > nba-stat-table > div.nba-stat-table > div.nba-stat-table__overflow > table > tbody > tr:nth-child({i+1})"
                row = driver.find_element_by_css_selector(selector)
            except:
                break
            
            name = row.find_element_by_class_name(selector_dic['player']).text
            stats = row.text.split('\n')[-1].split(' ')
            STATS.append([name]+stats)
            DATA[name] = [name]+stats
        if p <= selector_dic['nb pages']-2:
            next_page = driver.find_element_by_css_selector("body > main > div > div > div.row > div > div > nba-stat-table > div:nth-child(1) > div > div > a.stats-table-pagination__next")
            next_page.click()   

    df = pd.DataFrame(DATA)
    df.index = columns
    df = df.transpose()
    df.index = [i for i in range(df.shape[0])]

    return df



    

if __name__ == '__main__':

    # Dictionnaires de scrapping
    
    # Pour scrapper une nouvelle table, il suffit de rajouter un dictionnaire avec les bonnes infos :
    # url : url de la table
    # name : nom du fichier csv enregistré (on s'en fout un peu, faut juste que ce soit comprehensible)
    # nb pages : nombre de pages de la table
    # player : nom de la classe qui contient le nom des joueurs :
    #    - Aller sur une ligne de stats de la table
    #    - Inspecter
    #    - Remonter un peu avec la souris jusqu'à avoir le nom du joueur/équipe séléctionné par l'outil d'inspection
    #    (Ok c'est pas clair mais bon...)

    selector_dic_players_trad = {}
    selector_dic_players_trad['url'] = "https://www.nba.com/stats/players/traditional/?sort=PTS&dir=-1"
    selector_dic_players_trad['name'] = "stats_players_trad"
    selector_dic_players_trad['player'] = "player"
    selector_dic_players_trad['nb pages'] = 10
    
    selector_dic_players_advanced = {}
    selector_dic_players_advanced['url'] = "https://www.nba.com/stats/players/advanced/?sort=GP&dir=-1"
    selector_dic_players_advanced['name'] = "stats_players_advanced"
    selector_dic_players_advanced['player'] = "first"
    selector_dic_players_advanced['nb pages'] = 10

    selector_dic_players_scoring = {}
    selector_dic_players_scoring['url'] = "https://www.nba.com/stats/players/scoring/?sort=GP&dir=-1"
    selector_dic_players_scoring['name'] = "stats_players_scoring"
    selector_dic_players_scoring['player'] = "first"
    selector_dic_players_scoring['nb pages'] = 10

    selector_dic_players_usage = {}
    selector_dic_players_usage['url'] = "https://www.nba.com/stats/players/usage/?sort=GP&dir=-1"
    selector_dic_players_usage['name'] = "stats_players_usage"
    selector_dic_players_usage['player'] = "first"
    selector_dic_players_usage['nb pages'] = 10

    selector_dic_team_trad = {}
    selector_dic_team_trad['url'] = "https://www.nba.com/stats/teams/traditional/?sort=W_PCT&dir=-1"
    selector_dic_team_trad['name'] = "stats_teams_trad"
    selector_dic_team_trad['player'] = "first"
    selector_dic_team_trad['nb pages'] = 1

    selector_dic_team_advanced = {}
    selector_dic_team_advanced['url'] = "https://www.nba.com/stats/teams/advanced/?sort=W&dir=-1"
    selector_dic_team_advanced['name'] = "stats_teams_advanced"
    selector_dic_team_advanced['player'] = "team-name.first"
    selector_dic_team_advanced['nb pages'] = 1

    # Chose dictionnary to scrape
    selector_dic = selector_dic_players_usage
    
    # Scrape statistic table
    df = get_players_stats(selector_dic)

    # Store dataframe to csv file
    df.to_csv("datasets/"+selector_dic['name']+'.csv')
    df = pd.read_csv("datasets/"+selector_dic['name']+'.csv').drop(["Unnamed: 0"], axis=1)

    # Print dataframe
    print(df)

    




    








    
