import sys
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from tqdm import tqdm
import json 
import league_api
import importlib
importlib.reload(league_api)

def create_database(database_name):
    try:
        database = client.create_database(database_name)
    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(database_name)
    return database

def create_container(database, container_name):
    try:
        container = database.create_container(id=container_name,    partition_key=PartitionKey(path="/league"))
    except exceptions.CosmosResourceExistsError:
        container = database.get_container_client(container_name)
    except exceptions.CosmosHttpResponseError:
        raise
    return container

def get_database(database_name):
    return client.get_database_client(database_name)

def get_container(database, container_name):
    return database.get_container_client(container_name)

def insert_item(container,data):
    container.upsert_item(data)

def get_games_1_player(summonerId,game_num):
    player_dict = {}
    player_dict['id'] = str(summonerId)
    account_id = league.get_account_id(summonerId)
    player_mastery = league.get_champion_mastery(summonerId)
    player_dict['mastery'] = player_mastery
    match_hist = league.get_player_match_hist(account_id)
    all_other_players = []
    final_matches = []
    for match in match_hist[:game_num]:
        game_stats = league.get_game_stats(match)
        try:
            match_dict = {}
            match_dict["id"] = str(game_stats['gameId'])
            match_dict["stats"] = game_stats
            players_in_game = league.get_players_id_1_match(game_stats,exclude=summonerId) 
            #exclude the player that call the query
            all_other_players += players_in_game
            insert_item(match_container,match_dict)
            final_matches.append(match_dict['id'])
        except:
            print("cant get match hist for this")
            pass
    all_other_players = list(set(all_other_players)) #list of players play with the current summonerId
    player_dict['matches'] = final_matches
    insert_item(player_container,player_dict) #send to cosmos
    return all_other_players,len(final_matches)


if __name__ == "__main__": #main function to run python
    #credential
    ACCOUNT_URI = "https://lolpredict.documents.azure.com:443/"
    ACCOUNT_KEY = "UcLcT6bvFUsk677XfibNhJIIqiAstRkaWWrqTJaQOCmVqx0IN0J1ufYdpbsarowutD6nMSKaaLS1NqcD0QDIdQ=="
    client = CosmosClient(ACCOUNT_URI, credential=ACCOUNT_KEY)

    database = get_database("league_all_data")

    # create container 
    player_container = create_container(database,"players")
    match_container = create_container(database,"matches")

    #got list of players of diamond I
    league = league_api.LeagueAPI()
    league.set_key("RGAPI-82ec18c1-a18d-469d-b54e-04b5da131794")
    player_list = league.get_player_list("DIAMOND","I")

    #run the main program
    match_count = 0
    for player in tqdm(player_list):
        print("seed user {}".format(player))
        all_other_players,len_matches = get_games_1_player(player,10)
        placeholder = None
        print("query {} other players".format(len(all_other_players)))
        for o_pl in all_other_players: #for each other player, query 5 matches
            placeholder = get_games_1_player(o_pl,5)
        match_count += len_matches
        print("Done for user {}, now we have {} full matches".format(player,match_count))
