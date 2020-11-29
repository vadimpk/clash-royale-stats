"""
This is stuff I don't use but it is working
"""

def get_grand_challenge_battles(tag):
    
    endpoint = "/players/{}{}/battlelog".format(hashtag, tag)
    data = get_raw_data(endpoint)

    if data:

        battles = []
        for battle in data:
            if battle["type"] == "challenge" and battle["challengeTitle"] == "Grand Challenge":
                battles.append(battle)

        return battles

    else:
        return None

def get_badges(tag):
    
    endpoint = "/players/{}{}".format(hashtag, tag)
    data = get_raw_data(endpoint)

    if data:

        badges = data["badges"]
        return badges

    else:
        return None



def check_grand_challenge_battles(tag):

    players_collection = db["grand_challenge_players"]
    if not players_collection.find_one({"tag": tag}):
            if is_grand_challenge_player(tag):
                players_collection.insert_one({"tag": tag, "lastBattleTime": ""})

    result_collection = db["grand_challenge_results"]
    battles = get_grand_challenge_battles(tag)

    # get only new battles (to avoid parsing the same battles more than once)
    # there is a last_battle_time variable stored in player collection, which is
    # updated after every check_grand_challenge_battles function call
    # and is set to "" by default, when the player is first added
    last_battle_time = players_collection.find_one({"tag": tag})["lastBattleTime"]
    battles = check_new_battles(battles, last_battle_time)

    for battle in battles:
        data = parse_grand_challenge_battle(battle)
        
        if not result_collection.find_one({"deckId":data["mDeckName"]}):
            
            result_collection.insert_one({
                "deckId": data["mDeckName"],
                "wins": 0,
                "loses": 0,
                "draws": 0,
                "decksPlayedAgainst": {}
                })

        deck_info = result_collection.find_one({"deckId":data["mDeckName"]})

        if data["oDeckName"] not in deck_info["decksPlayedAgainst"]:
            deck_info["decksPlayedAgainst"][data["oDeckName"]] = {
                "wins": 0,
                "loses": 0,
                "draws": 0,
            }

        if data["result"] == "w":
            deck_info["wins"] += 1
            deck_info["decksPlayedAgainst"][data["oDeckName"]]["wins"] += 1
        
        elif data["result"] == "l":
            deck_info["loses"] += 1
            deck_info["decksPlayedAgainst"][data["oDeckName"]]["loses"] += 1

        else:
            deck_info["draws"] += 1
            deck_info["decksPlayedAgainst"][data["oDeckName"]]["draws"] += 1

        result_collection.update_one({"deckId": data["mDeckName"]}, {"$set": {
            "wins": deck_info["wins"],
            "loses": deck_info["loses"],
            "draws": deck_info["draws"],
            "decksPlayedAgainst": deck_info["decksPlayedAgainst"]
            }})

        if not players_collection.find_one({"tag": data["oTag"]}):
            if is_grand_challenge_player(data["oTag"]):

                players_collection.insert_one({"tag": data["oTag"], "lastBattleTime": ""})

        last_battle_time = battle["battleTime"]
        
    players_collection.update_one({"tag": tag}, {"$set": {"lastBattleTime": last_battle_time}})

def is_grand_challenge_player(tag):
    
    player_badges = get_badges(tag)

    for badge in player_badges:
        if badge["name"] == "Grand12Wins":
            return True
    
    else:
        return None


def parse_grand_challenge_battle(battle):

    m_deck = []
    o_deck = []
    m_deck_name = ""
    o_deck_name = ""

    o_tag = battle["opponent"][0]["tag"][1:]

    for card in battle["team"][0]["cards"]:
        m_deck.append((card["id"], 9))

    for card in battle["opponent"][0]["cards"]:
        o_deck.append((card["id"], 9))

    m_deck.sort()
    o_deck.sort()

    # loop through sorted deck to create a uniq name
    for card in m_deck:
        m_deck_name += str(card[0])
    for card in o_deck:
        o_deck_name += str(card[0])

    if battle["team"][0]["crowns"] > battle["opponent"][0]["crowns"]:
        result = "w"

    elif battle["team"][0]["crowns"] < battle["opponent"][0]["crowns"]:
        result = "l"

    else:
        result = "d"

    context = {
        "mDeckName": m_deck_name,
        "oDeckName": o_deck_name,
        "mDeck": m_deck,
        "oDeck": o_deck,
        "result": result,
        "oTag": o_tag,
        "battleTime": battle["battleTime"]
    }

    return context

