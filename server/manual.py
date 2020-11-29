from manual_functions import add_player, start_new_season, delete_all, delete_one_player
from get_data import get_clan_members
from connect_db import db

def main():

    print("Choose an option:\nstart new season (sns)\nadd player (ap)\nadd clan (ac)\ndelete player (dp)\ndelete clan (dc)\ndelete all (da)\nparse unparsed (pu)")

    answer = input()

    if answer == "sns":
        start_new_season()

    elif answer == "ap":

        print("type player tag")
        tag = input()
        add_player(tag)

    elif answer == "ac":

        print("type clan tag")

        tag = input()

        players = get_clan_members(tag)
        for player in players:
            add_player(player)

    elif answer == "dp":

        print("type player tag")
        tag = input()
        print("are you sure?")
        answer = input()
        if answer == "yes":

            print("seriously?")
            answer = input()

            if answer == "YES":
                print("okay, okay")
        delete_one_player(tag)
        
    elif answer == "dc":

        print("type clan tag")
        tag = input()
        players = get_clan_members(tag)

        for player in players:

            delete_one_player(player)

    elif answer == "da":

        print("are you sure?")
        answer = input()
        if answer == "yes":

            print("seriously?")
            answer = input()

            if answer == "YES":
                print("okay, okay")
                delete_all()
    else: 
        print("incorrect. try again")

if __name__ == "__main__":

    main()
