from connect_db import db

players = db.players.find()

battles = 0
def get_player_battles_amount(tag):

    collection1 = db["p_"+tag+"_battles"]
    collection2 = db["p_"+tag+"_battles_challenge"]
    collection3 = db["p_"+tag+"_battles_2v2"]

    ladder_battles = collection1.count_documents({})
    challenge_battles = collection2.count_documents({})
    casual2v2_battles = collection3.count_documents({})

    return ladder_battles, challenge_battles, casual2v2_battles

def print_battles_amount():

    for player in players:

        collection = db["p_"+player["tag"]+"_battles"]
        ladder_battles, challenge_battles, casual2v2_battles = get_player_battles_amount(player["tag"])

        print(f"{collection.find({'_id':collection.count_documents({})})[0]['team'][0]['name']}:")
        print(f"\tladder battles: {ladder_battles}")
        print(f"\tchallenge battles: {challenge_battles}")
        print(f"\t2v2 battles: {casual2v2_battles}")
        print(f"\ttotal battles: {ladder_battles + challenge_battles + casual2v2_battles}")
