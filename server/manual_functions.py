from connect_db import db
from datetime import datetime

from parse_battles import parse_1v1_battle, parse_2v2_battle
from get_data import get_player_battlelog, check_if_player_exist, get_player_PB_and_level, get_seasonal_data


def add_player(tag):

    if check_if_player_exist(tag):

        if not db.players.find_one({"tag":tag}):

            now = datetime.now()
            db.players.insert_one({ "tag": tag, "active": True, "date": now})

            player_collection = db["p_"+tag]
            season = db.seasons.find_one({"_id":db.seasons.count()})
            season_name = "season" + str(int(season["season"]))
            season_info = get_seasonal_data(tag)
            player_collection.insert_one({"name":"seasonsInfo", season_name: season_info})
            player_collection.insert_one({"name":"dailyInfo", "dates":{}})

            #loop through 3 types of battles
            for i in range(3):
                if i == 0:
                    battles_collection = db["p_" + tag + "_battles"]
                    battle_type = "Ladder"
                    parsing_function = parse_1v1_battle

                elif i == 1:
                    battles_collection = db["p_" + tag + "_battles_challenge"]
                    battle_type = "Challenge"
                    parsing_function = parse_1v1_battle

                else:
                    battles_collection = db["p_" + tag + "_battles_2v2"]
                    battle_type = "2v2"
                    parsing_function = parse_2v2_battle

                battles = get_player_battlelog(tag, battle_type)

                if battles != []:
                    m_info = get_player_PB_and_level(tag)

                count_battles = 0

                for battle in battles:
                    
                    battle["_id"] = len(battles) - count_battles
                    count_battles += 1
                    battle["season"] = int(season["season"])
                    battle = parsing_function(battle, m_info, battle_type)
                    battles_collection.insert_one(battle)

            print("player " + tag + " added")

        else:
            print("player already exists")
    
    else:
        print("invalid tag")

def start_new_season():

    last_season_id = db.seasons.count()
    last_season = db.seasons.find_one({"_id": last_season_id})
    db.seasons.insert_one({"_id": last_season_id + 1, "season": int(last_season["season"]) + 1})
    players = db.players.find()
    current_season = "season" + str(int(last_season["season"]) + 1)

    for player in players:
        
        season_info = get_seasonal_data(player["tag"])
        player_collection = db["p_" + player["tag"]]

        player_collection.update_one({"name":"seasonsInfo"}, {"$set": {current_season: season_info}})

def delete_one_player(tag):
    
    players = db.players.find()

    player_collections = [
        db["p_"+str(tag)+"_battles"],
        db["p_"+str(tag)],
        db["p_"+str(tag)+"_battles_challenge"],
        db["p_"+str(tag)+"_battles_2v2"]
    ]
        
    for collection in player_collections:
        collection.drop()

    db.players.remove({"tag":tag})

def delete_all():

    players = db.players.find()

    for player in players:

        player_collections = [
            db["p_"+player["tag"]+"_battles"],
            db["p_"+player["tag"]],
            db["p_"+player["tag"]+"_battles_challenge"],
            db["p_"+player["tag"]+"_battles_2v2"]
        ]
        
        for collection in player_collections:
            collection.drop()

    db.players.drop()






