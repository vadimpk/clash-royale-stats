from connect_db import db

players = db.players.find()

def delete_player(tag):

    collection = db["p_"+tag+"_battles"]
    collection2 = db["p_"+tag]
    collection3 = db["p_"+tag+"_battles_challenge"]
    collection4 = db["p_"+tag+"_battles_2v2"]

    collection.drop()
    collection2.drop()
    collection3.drop()
    collection4.drop()
    db.players.delete_one({ "tag": tag })

def clear_players():

    for player in players:

        collection = db["p_"+player["tag"]+"_battles"]
        collection2 = db["p_"+player["tag"]+"_battles_challenge"]
        collection3 = db["p_"+player["tag"]+"_battles_2v2"]
            
        print(f"{collection.find({'_id':collection.count_documents({})})[0]['team'][0]['name']}:")
        print(f"\tladder battles: {collection.count_documents({})}")
        print(f"\tchallenge battles: {collection2.count_documents({})}")
        print(f"\t2v2 battles: {collection3.count_documents({})}") 
        print("do you want to delete this player?(y/n)")

        ans = input()

        if ans == "y":

            delete_player(player["tag"])
            

