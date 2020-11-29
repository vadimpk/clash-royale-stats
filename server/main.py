from server_functions import check_battles, collect_daily_data
from connect_db import db

def main():

    players = db.players.find()

    season_id = db.seasons.find_one({"_id":db.seasons.count_documents({})})["season"]

    for player in players:
        
        if player["active"] == True:
        
            check_battles(player["tag"], int(season_id), "Ladder")
            collect_daily_data(player["tag"], int(season_id))

            check_battles(player["tag"], int(season_id), "Challenge")
            check_battles(player["tag"], int(season_id), "2v2")

if __name__ == "__main__":

    main()