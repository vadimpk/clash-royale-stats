from connect_db import db
from datetime import datetime

from parse_battles import parse_1v1_battle, parse_2v2_battle
from get_data import get_player_battlelog, get_player_PB_and_level, get_daily_data

def check_battles(tag, season_id, battle_type):
    
    try:

        if battle_type == "Ladder":
            battles_collection = db["p_"+tag+"_battles"]
            parsing_function = parse_1v1_battle

        elif battle_type == "Challenge":
            battles_collection = db["p_"+tag+"_battles_challenge"]
            parsing_function = parse_1v1_battle

        elif battle_type == "2v2":
            battles_collection = db["p_"+tag+"_battles_2v2"]
            parsing_function = parse_2v2_battle

        battles = get_player_battlelog(tag, battle_type)
        added_battles = 0

        if battles != []:
            count_battles = battles_collection.count()

            # if it's the first battle there is no need to check whether it is new
            if count_battles == 0: 
                # we get m_info here to save some time 
                # (instead of calling every time in parse_battle function)
                m_info = get_player_PB_and_level(tag)
                
                for battle in battles:

                    battle["_id"] = len(battles) - count_battles
                    battle["season"] = season_id

                    battle = parsing_function(battle, m_info, battle_type)
                    battles_collection.insert_one(battle)

                    count_battles += 1
                    added_battles += 1

            # if it's not the first battle
            else:

                # we need to get only new battles
                last_battle_time = battles_collection.find_one({"_id":count_battles})["battleTime"]
                new_battles = check_new_battles(battles, last_battle_time)

                if new_battles != []:
                    m_info = get_player_PB_and_level(tag)

                    for battle in new_battles:

                        battle["_id"] = count_battles + 1
                        battle["season"] = season_id

                        battle = parsing_function(battle, m_info, battle_type)
                        battles_collection.insert_one(battle)

                        count_battles += 1
                        added_battles += 1

        print("added", added_battles, battle_type, "battles for", tag)
    except:
        print("error occured while parsing ladder battles for" + str(tag))

def check_new_battles(battles, last_battle_time):

    new_battles = []
    for battle in battles:

        if last_battle_time == battle["battleTime"]:
            break

        new_battles = [battle] + new_battles
    return new_battles

def collect_daily_data(tag, season_id):

    today = datetime.today().strftime('%Y-%m-%d')

    player_collection = db["p_"+tag]
    player_dates = player_collection.find_one({"name":"dailyInfo"})["dates"]

    if today not in player_dates.keys():
        try:
            daily_info = get_daily_data(tag)

            daily_info["date"] = today
            daily_info["season"] = season_id

            player_dates[today] = daily_info
            player_collection.update_one({"name":"dailyInfo"}, {"$set":{"dates": player_dates}})

        except:
            pass

