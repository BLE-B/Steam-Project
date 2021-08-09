import json
import urllib.request
import pandas as pd
from urllib.error import HTTPError




profile_url = 'http://steamcommunity.com/id/gabelogannewell'

url_start = 'http://api.steampowered.com/ISteamUser/'

request_group_list = ['ISteamUser', 'ISteamUserStats', 'IPlayerService']
request_type_list = ['GetPlayerSummaries', 'GetFriendList', 'GetOwnedGames', 'GetRecentlyPlayedGames']
v_type_list = ['v0001', 'v0002']

def get_player_ID(profile_url):
    if profile_url[-1] == '/':
        profile_url = profile_url[0:-1]
    player_ID = profile_url.split('/')[-1]
    return player_ID

def get_profile_url(player_ID):
    url = 'https://www.steamcommunity.com/profiles/' + player_ID
    return url

player_ID = get_player_ID(profile_url)

def get_player_url(request_group, request_type, v_type, key, params, url_start = 'https://api.steampowered.com'):
    param_line = ''
    #print('params:', params)
    for keys, values in params.items():
        if keys != 'steamids':
            param_line = param_line + '&' + keys + '=' + values
            #print(param_line)
        elif keys == 'steamids' and type(values) == str:
            param_line = param_line + '&' + keys + '=' + values
            #print(param_line)
        else:
            temp = '['
            for valu in values:
                temp = temp + valu + ','
            temp = temp[:-1]
            temp = temp + ']'
            param_line = param_line + '&' + keys + '=' + temp
            #print(param_line)
    request = '?key=' + key + param_line
    webURL = '/'.join([url_start, request_group, request_type, v_type, request])
    #print('webURL: ', webURL)
    return webURL

def url_to_json(url):
    try:
        webURL = urllib.request.urlopen(url)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        json_obj = json.loads(data.decode(encoding))
        return json_obj
    except:
        #print(urllib.request.urlopen(url).get_code())
        print('Something went wrong')
        pass


def get_player_summaries(player_ID, key):
    request_group = request_group_list[0]
    request_type = request_type_list[0]
    v_type = v_type_list[1]
    params = {'steamids':player_ID}
    print('params', len(params['steamids']))
    url = get_player_url(request_group, request_type, v_type, key, params)
    data = url_to_json(url)
    print('len data', len(data['response']['players']))
    return data
    
def get_friend_list(player_ID, key):
    request_group = request_group_list[0]
    request_type = request_type_list[1]
    v_type = v_type_list[0]
    params = {'steamid':player_ID, 'relationship':'friend'}
    url = get_player_url(request_group, request_type, v_type, key, params)
    data = url_to_json(url)
    try:
        #print(player_ID, data['friendslist']['friends'][0])
        gaggabagga = data['friendslist']['friends'][0]
    except TypeError:
        #print(player_ID, 'empty')
        data = None
        pass
    return data
    
def get_owned_games(player_ID, key):
    request_group = request_group_list[2]
    request_type = request_type_list[2]
    v_type = v_type_list[0]
    params = {'steamid':player_ID, 'format':'json'}
    url = get_player_url(request_group, request_type, v_type, key, params)
    data = url_to_json(url)
    return data
    
def get_recently_played_games(player_ID, key):
    request_group = request_group_list[2]
    request_type = request_type_list[3]
    v_type = v_type_list[0]
    params = {'steamid':player_ID, 'format':'json'}
    url = get_player_url(request_group, request_type, v_type, key, params)
    data = url_to_json(url)
    return data