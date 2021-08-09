import json
import pandas as pd
import re

import steam_api_official as steam_api



def add_player_to_df(player_ID, key, players_df, friend_distance):
    player_data = [player_ID]

    play_sum_data = steam_api.get_player_summaries(player_ID, key)
    #print('play_sum_data for player ID', player_ID)
    #with open('json_files/player_summary_'+player_ID+'.json', 'w') as f:
    with open('json_files/player_summary.json', 'w') as f:
        json.dump(play_sum_data, f)
        
    friend_data = steam_api.get_friend_list(player_ID, key)
    #print('friend_data for player ID', player_ID)
    #with open('json_files/player_friends_'+player_ID+'.json', 'w') as f:
    with open('json_files/player_friends.json', 'w') as f:
        json.dump(friend_data, f)

    owned_games_data = steam_api.get_owned_games(player_ID, key)
    #print('owned_games_data for player ID', player_ID)
    #with open('json_files/owned_games_'+player_ID+'.json', 'w') as f:
    with open('json_files/owned_games.json', 'w') as f:
        json.dump(owned_games_data, f)
    
    recently_played_data = steam_api.get_recently_played_games(player_ID, key)
    #print('recently_played_data for player ID', player_ID)
    #with open('json_files/recent_games_'+player_ID+'.json', 'w') as f:
    with open('json_files/recent_games.json', 'w') as f:
        json.dump(recently_played_data, f)
    
    #with open('json_files/player_summary_'+player_ID+'.json', 'r') as f:
    with open('json_files/player_summary.json', 'r') as f:
        data = json.load(f)
    dic_entries = ['personaname', 'realname', 'loccountrycode', 'timecreated']
    for entry in dic_entries:
        if entry in data['response']['players'][0]:
            player_data.append(data['response']['players'][0][entry])
        else:
            player_data.append(None)

    #with open('json_files/player_friends_'+player_ID+'.json', 'r') as f:      
    with open('json_files/player_friends.json', 'r') as f:
        data = json.load(f)
    if data != None:
        player_data.append(data['friendslist']['friends'])
    else:
        player_data.append(None)

    player_data.append(friend_distance)
    
    #print('player data:', player_data)
    
    player_df = pd.DataFrame([player_data], columns = ['player_id', 'nick', 'name', 'country', 'acc_creation', 'friends_ids', 'friend_dist'])
    if player_ID not in players_df['player_id'].values:
        players_df = players_df.append(player_df, ignore_index = True)
   
    return players_df


def add_players_to_df(player_ID, key, players_df, friend_distance, q_1 = True):
    player_data = player_ID
    
    if q_1:
        play_sum_data = steam_api.get_player_summaries(player_ID, key)
        print('len sum data', len(play_sum_data['response']['players']))
        print(play_sum_data)
        #print('play_sum_data for player ID', player_ID)
        #with open('json_files/player_summary_'+player_ID+'.json', 'w') as f:
        with open('json_files/player_summary.json', 'w') as f:
            json.dump(play_sum_data, f)
    
    #with open('json_files/player_summary_'+player_ID+'.json', 'r') as f:
    with open('json_files/player_summary.json', 'r') as f:
        data = json.load(f)
    dic_entries = ['personaname', 'realname', 'loccountrycode', 'timecreated']
    for count, player in enumerate(player_data):
        print('count', count)
        print(player)
        player_data = [player]
        for entry in dic_entries:
            if entry in data['response']['players'][count]:
                player_data.append(data['response']['players'][count][entry])
            else:
                player_data.append(None)    
        player_data.append(None)
        player_data.append(friend_distance)
        #print('player data:', player_data)
        player_df = pd.DataFrame([player_data], columns = ['player_id', 'nick', 'name', 'country', 'acc_creation', 'friends_ids', 'friend_dist'])
        if player not in players_df['player_id'].values:
            players_df = players_df.append(player_df, ignore_index = True) 

    #print('palyers_df:', players_df)
    return players_df


def gen_entries(players_df, key):
    ### generate db entries with friend IDs
    for i in range(len(players_df['friends_ids'][0])):
        temp_id_list = []
        temp_id = players_df['friends_ids'][0][i]['steamid']
        temp_id_list = temp_id_list.append(temp_id)
        players_df = add_player(temp_id, key, players_df, False)
        
def add_player(player_ids, key, players_df, friend_distance):
    if type(player_ids) == list:
        players_df = add_players_to_df(player_ids, key, players_df, friend_distance, True)
    else:
        players_df = add_player_to_df(player_ids, key, players_df, friend_distance)
    return players_df

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))



def create_network(player_ID, df, base_df, players_df, key, depth = 1):
    print('depth', depth)
    if len(df) == 0:
        df = add_player(player_ID, key, df, 0)
    
    #if len(base_df) == 0:
    base_df = df
        
    # iteration 1: df = base_df = df with len 1
    # iteration 2: df = base_df = new_df (second_df)
    
    second_df = blank_df
    
    #print('base_df length:', len(base_df))
    friend_distance = max(0, base_df['friend_dist'].max() + 1)

    for x in range(len(df)):
        # df['friends_ids'][x] - list of friend dicts (3 entries each)
        # df['friends_ids'] - pd Series with x entries of above lists
        # df.loc[x, 'friends_ids'] - list of friend dicts (3 entries each)
        # df.loc[x, 'friends_ids'][0] - first dict of above list
        # df.loc[x, 'friends_ids'][0][0] - steamID of first dict of above list
        # steam_api.get_friend_list(df['player_id'][x], key)['friendslist']['friends'] - list of friend dicts
        try:
            df['friends_ids'][x] = steam_api.get_friend_list(df['player_id'][x], key)['friendslist']['friends']
        except TypeError:
            df['friends_ids'][x] = None
        #print(df.friends_ids.head())
        friends_ids = []
        try:
            for bla in df.loc[x, 'friends_ids']:
                #print(x, bla)
                hugo = bla['steamid']
                friends_ids.append(hugo)
            #print(friends_ids)
            chunked_friends = list(chunks(friends_ids, 100))
            first_df = blank_df
            for sublist in range(len(chunked_friends)):
                first_df = add_player(chunked_friends[sublist], key, first_df, friend_distance)
                #print('first de eff:', first_df)
            friendlist_dict = {}
            if depth > 1:
                for friend in friends_ids:
                    data = steam_api.get_friend_list(friend, key)
                    if data != None:
                        friendlist_dict[friend] = data['friendslist']['friends']
                    else:
                        friendlist_dict[friend] = None
                first_df['friends_ids'] = first_df['player_id'].map(friendlist_dict)
            second_df = second_df.append(first_df, ignore_index = True)
        except TypeError:
            print('Erreur du passe!')
            pass
    if len(players_df) == 0:
        players_df = base_df.append(second_df, ignore_index = True)
    else:
        players_df = players_df.append(second_df, ignore_index = True)
    player_ID = list(second_df['player_id'])
    if depth > 1:
        #print('playerssssssssss', players_df)
        create_network(player_ID, second_df, base_df, players_df, key, depth - 1)
    else:
        players_df.to_json('players.json')
        players_df.to_csv('players.csv')
    
        return players_df
    

if __name__ == '__main__':
    key = input('Please insert key: ')
    profile_url = input('please insert profile URL: ')

    player_ID = steam_api.get_player_ID(profile_url)

    blank_df = pd.DataFrame(columns = ['player_id', 'nick', 'name', 'country', 'acc_creation', 'friends_ids', 'friend_dist'])
    
    players_df = create_network(player_ID, blank_df, blank_df, blank_df, key, 2)