import requests 
import json 
import time
class LeagueAPI():
    def __init__(self):
        self.api_key = None
        self.params = {"api_key":self.api_key}
        self.base_url = "https://na1.api.riotgames.com/lol" #base url

    def reset_key(self):
        print("Key expired!")
        val = input("Enter new api key value") #enter new API key to proceed
        self.set_key(val)

    def set_key(self,api_key):
        self.api_key = api_key
        self.params["api_key"] = self.api_key

    def get_player_list(self,rank,rank_num):
        url = "{}/league/v4/entries/RANKED_SOLO_5x5/{}/{}".format(self.base_url,
                                                                    str.upper(rank),str(rank_num))
        data = requests.get(url=url,params = self.params)
        time.sleep(1.3)
        if data.status_code == 200:
            self.player_list = set()
            data_json = json.loads(data.text)
            for player in data_json:
                self.player_list.add(player['summonerId'])
        elif data.status_code == 403: #need to reset API
            self.reset_key()
            self.get_player_list(rank,rank_num)

    def get_account_id(self,summonerId):
        url = "{}/summoner/v4/summoners/{}".format(self.base_url,summonerId)
        data = requests.get(url=url,params = self.params)
        time.sleep(1.3)
        if data.status_code == 200:
            data_json = json.loads(data.text)
            return data_json['accountId']
        elif data.status_code == 403:
            self.reset_key()
            self.get_account_id(summonerId) #restart
        else:
            print("cant find player id")
            return None
    
    def get_player_match_hist(self,accountId):
        url = "{}/match/v4/matchlists/by-account/{}".format(self.base_url,accountId)
        data = requests.get(url=url,params = self.params)
        time.sleep(1.3)
        if data.status_code == 200:
            match_list = []
            data_json = json.loads(data.text)
            for match in data_json['matches']:
                match_list.append(match['gameId'])
            return match_list
        elif data.status_code == 403:
            self.reset_key()
            self.get_player_match_hist(accountId) #restart
        else:
            print("cant find player history")
            return None

    def get_game_stats(self,gameId):
        url = "{}/match/v4/matches/{}".format(self.base_url,gameId)
        data = requests.get(url=url,params = self.params)
        time.sleep(1.3)
        if data.status_code == 200:
            data_json = json.loads(data.text)
            return data_json
        elif data.status_code == 403:
            self.reset_key()
            self.get_game_stats(gameId) #restart
        else:
            print("cant find game stats")
            return None

    def get_champion_mastery(self,summonerId): #only mastery point
        url = "{}/summoner/v4/summoners/{}".format(self.base_url,summonerId)
        data = requests.get(url=url,params = self.params)
        time.sleep(1.3)
        if data.status_code == 200:
            data_json = json.loads(data.text)
            mastery = {}
            for champ in data_json:
                mastery[champ['championId']] = champ['championPoints']
            return mastery
        elif data.status_code == 403:
            self.reset_key()
            self.get_champion_mastery(summonerId) #restart
        else:
            print("cant find champion mastery")
            return None