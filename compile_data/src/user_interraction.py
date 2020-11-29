from connect_db import db
import re
import dateutil.parser
import datetime
import pytz
import time

def check_tag(tag):

    collection_name = "p_"+tag

    if collection_name in db.list_collection_names():
        return True

    elif tag == "exit":
        print("\nbye..")
        return "exit"

    else:
        print("\nTag doesn't exist in database. Try again:\n")
        return False


def get_possible_periods(tag):

    player_collection = db["p_"+tag]
    seasonal_info = player_collection.find_one({"name":"seasonsInfo"})

    options = [
        "all time",
        "1 day",
        "3 days",
        "7 days",
        "21 days",
        "56 days"
    ]

    for season in seasonal_info:

        if "season" in season:
            season_id = re.findall(r"\d+", season)[0]
            options.append("season " + str(season_id))

    return options

def check_period(options, period):

    if period in options:
        print("\nWait a bit. Loading your statistics...")
        return True

    elif period == "exit":
        print("\nbye..")
        return "exit"

    else:
        print("\nIncorrect. Try again:\n")
        return False


def get_period_battles(period, tag):

    battles_collection = db["p_"+tag+"_battles"]

    if "season" in period:

        season_id = re.findall(r"\d+", period)[0]

        battles = [x for x in battles_collection.find({"season":int(season_id), "parsed":True})]

    elif period == "all time":

        battles = [x for x in battles_collection.find({"parsed":True})]

    else:

        number_of_days = int(re.findall(r"\d+", period)[0])
        all_battles = battles_collection.find({"parsed":True})
        battles = []

        for battle in all_battles:

            date = battle["battleTime"]
            difference = pytz.utc.localize(datetime.datetime.utcnow()) - dateutil.parser.isoparse(date)

            if difference.days < number_of_days:
                battles.append(battle)

    return battles


def get_user_request():

    # getting user's tag and validate it
    print("\nType your tag:")
    print("or type 'exit' to leave.\n")

    answered = False
    while not answered:

        tag = input()
        answered = check_tag(tag) # it's either False or True (or 'exit')
        time.sleep(0.2)

        if answered == "exit":
            return

    # getting user's period and validate it
    print("\nChoose your period:")
    print("or type 'exit' to leave.\n")

    answered = False
    while not answered:

        # these data can vary depending on when the tag was added into the database
        # so we need to get options for specific tag every time
        options = get_possible_periods(tag)

        time.sleep(1.2)
        for option in options:
            print(option)
        print()

        period = str(input())
        answered = check_period(options, period) # it's either False or True (or 'exit')
        time.sleep(0.2)

        if answered == "exit":
            return

    # getting battles depending on period
    return get_period_battles(period, tag), tag, period


