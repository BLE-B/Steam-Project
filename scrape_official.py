import json
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

import steam_api_official as steam_api


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def get_bio(json_data = 'players.json'):
    with open(json_data, 'r') as f:
        data = json.load(f)
    players_df = pd.DataFrame.from_dict(data)
    #print(players_df.info())
    
    url_list = []
    for ids in players_df['player_id']:
        url = steam_api.get_profile_url(ids)
        #print(url)
        url_list.append(url)
        
    players_df['url'] = url_list
    
    #url_list = url_list[0:10]
    
    bios = []
    for ele in url_list:
        r = requests.get(ele)
        soup = BeautifulSoup(r.text, 'html.parser')
        stuff = soup.find('div', class_='profile_summary')
        #print(ele, stuff)
        if stuff == '':
            stuff = ['Private profile']
        bios.append(stuff)
    
    
    clean_bios = []
    for ele in bios:
        clean_bios.append(cleanhtml(str(ele)))
        
    print(clean_bios)
    
    blalist = []
    for ele in clean_bios:
        escapes = ''.join([chr(char) for char in range(1, 32)])
        translator = str.maketrans({ord(char): None for char in escapes})
        stuffi = ele.translate(translator)
        blalist.append(stuffi)
        
    print(blalist)
    
    players_df['bio'] = blalist
    
    
    
    players_df.to_json('players_with_bio.json')
    players_df.to_csv('players_with_bio.csv')
    
    

if __name__ == '__main__':
    get_bio()