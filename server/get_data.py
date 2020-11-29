from datetime import datetime
import urllib.request
import json

with open("crstats-server/token.txt") as f:
    token = f.read().rstrip("\n")

baseUrl = "https://api.clashroyale.com/v1"

hashtag = "%23"

def get_raw_data(endpoint):

    try:
        request = urllib.request.Request(
                baseUrl + endpoint,
                None,
                {
                    "Authorization": "Bearer %s" % token
                }
            )
        response = urllib.request.urlopen(request).read().decode("utf-8")
        return json.loads(response)
    except:
        return None

def check_if_player_exist(tag):
    # tag without hashtag (ex: CRVYJ0JJ)

    endpoint = "/players/{}{}".format(hashtag, tag)

    data = get_raw_data(endpoint)
    if data:
        return True
    else:
        return None

def get_player_PB_and_level(tag):

    endpoint = "/players/{}{}".format(hashtag, tag)
    data = get_raw_data(endpoint)

    if data:

        context = {
            "level": data["expLevel"],
            "bestTrophies": data["bestTrophies"]
        }

        return context
    else:
        return None

def get_seasonal_data(tag):

    endpoint = "/players/{}{}".format(hashtag, tag)
    data = get_raw_data(endpoint)

    if data:

        cards = {}
        for card in data["cards"]:
            card_level = card["level"] + (13 - card["maxLevel"])
            cards["c_"+str(card["id"])] = (card_level, card["count"])

        context = {
            "bestTrophies": data["bestTrophies"],
            "level": data["expLevel"],
            "wins": data["wins"],
            "losses": data["losses"],
            "battleCount": data["battleCount"],
            "totalDonations": data["totalDonations"],
            "cards": cards,
        }
        try:
            context["endingSeasonTrophies"] = data["leagueStatistics"]["previousSeason"]["trophies"]
            context["bestSeasonTrophies"] = data["leagueStatistics"]["previousSeason"]["bestTrophies"]
        except:
            pass

        return context
    else:
        return None

def get_daily_data(tag):

    endpoint = "/players/{}{}".format(hashtag, tag)
    data = get_raw_data(endpoint)

    if data:

        context = {
            "bestTrophies": data["bestTrophies"],           
            "wins": data["wins"],
            "losses": data["losses"],
            "battleCount": data["battleCount"],
            "totalDonations": data["totalDonations"],
        }

        return context

    else:
        return None

def get_player_battlelog(tag, battles_type):
    # tag without hashtag (ex: CRVYJ0JJ)

    endpoint = "/players/{}{}/battlelog".format(hashtag, tag)
    data = get_raw_data(endpoint)

    if data:

        ladder_battlelog = []
        challenge_battlelog = []
        casual_2v2_battlelog = []

        for battle in data:

            if battle["type"] == "PvP" and battles_type == "Ladder":
                ladder_battlelog.append(battle)

            elif battle["type"] == "challenge" and battles_type == "Challenge" and (battle["challengeTitle"] == "Classic Challenge" or battle["challengeTitle"] == "Grand Challenge"):
                challenge_battlelog.append(battle)

            elif battle["type"] == "casual2v2" and battles_type == "2v2":
                casual_2v2_battlelog.append(battle)

        if battles_type == "Ladder":
            return ladder_battlelog
        elif battles_type == "Challenge":
            return challenge_battlelog
        elif battles_type == "2v2":
            return casual_2v2_battlelog

    else:
        return None

def get_clan_members(tag):
    # tag without hashtag (ex: 2JVVC8QJ)

    endpoint = "/clans/{}{}/members".format(hashtag, tag)
    data = get_raw_data(endpoint)

    if data:
        players = []
        for player in data["items"]:
            players.append(player["tag"][1:])

        return players

    else:
        return None


