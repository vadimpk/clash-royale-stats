from connect_db import db
from get_data import get_player_PB_and_level


def parse_1v1_battle(battle, m_info, battle_type):

    try:

        m_deck = []
        o_deck = []
        m_cards_avg = 0
        o_cards_avg = 0

        o_info = get_player_PB_and_level(battle["opponent"][0]["tag"][1:])

        m_PB = m_info["bestTrophies"]
        o_PB = o_info["bestTrophies"]

        m_king_level = m_info["level"]
        o_king_level = o_info["level"]

        if battle_type == "Ladder":

            for card in battle["team"][0]["cards"]:

                card_level = card["level"] + (13 - card["maxLevel"])
                m_deck.append((card["id"], card_level))
                m_cards_avg += card_level / 8

            for card in battle["opponent"][0]["cards"]:

                card_level = card["level"] + (13 - card["maxLevel"])
                o_deck.append((card["id"], card_level))
                o_cards_avg += card_level / 8

        elif battle_type == "Challenge":

            for card in battle["team"][0]["cards"]:
                m_deck.append((card["id"], 9))

            for card in battle["opponent"][0]["cards"]:
                o_deck.append((card["id"], 9))

        m_deck.sort()
        o_deck.sort()

        del battle["opponent"][0]["cards"]
        del battle["team"][0]["cards"]

        if battle["team"][0]["crowns"] > battle["opponent"][0]["crowns"]:

            m_win = True

        elif battle["team"][0]["crowns"] < battle["opponent"][0]["crowns"]:

            m_win = False

        else:

            m_win = 0

        if battle_type == "Ladder":
            battle["team"][0].update({"mDeck":m_deck, "mCardsAvg":m_cards_avg, "mPB":m_PB, "mKingLevel":m_king_level, "mWin":m_win})
            battle["opponent"][0].update({"oDeck":o_deck, "oCardsAvg":o_cards_avg, "oPB":o_PB, "oKingLevel":o_king_level})

        elif battle_type == "Challenge":
            battle["team"][0].update({"mDeck":m_deck, "mPB":m_PB, "mKingLevel":m_king_level, "mWin":m_win})
            battle["opponent"][0].update({"oDeck":o_deck, "oPB":o_PB, "oKingLevel":o_king_level})

        battle["parsed"] = True
        return battle

    except:

        battle["parsed"] = False
        return battle

def parse_2v2_battle(battle, m_info_1, battle_type="2v2"):
    
    try:

        m_deck_1 = []
        o_deck_1 = []
        m_deck_2 = []
        o_deck_2 = []

        m_cards_avg_1 = 0
        m_cards_avg_2 = 0
        o_cards_avg_1 = 0
        o_cards_avg_2 = 0

        m_info_2 = get_player_PB_and_level(battle["opponent"][1]["tag"][1:])
        o_info_1 = get_player_PB_and_level(battle["opponent"][0]["tag"][1:])
        o_info_2 = get_player_PB_and_level(battle["opponent"][1]["tag"][1:])

        m_PB_1 = m_info_1["bestTrophies"]
        m_PB_2 = m_info_2["bestTrophies"]
        o_PB_1 = o_info_1["bestTrophies"]
        o_PB_2 = o_info_2["bestTrophies"]

        m_king_level_1 = m_info_1["level"]
        m_king_level_2 = m_info_2["level"]
        o_king_level_1 = o_info_1["level"]
        o_king_level_2 = o_info_2["level"]

        for card in battle["team"][0]["cards"]:
    
            card_level = card["level"] + (13 - card["maxLevel"])
            m_deck_1.append((card["id"], card_level))
            m_cards_avg_1 += card_level / 8

        for card in battle["team"][1]["cards"]:
        
            card_level = card["level"] + (13 - card["maxLevel"])
            m_deck_2.append((card["id"], card_level))
            m_cards_avg_2 += card_level / 8

        for card in battle["opponent"][0]["cards"]:
        
            card_level = card["level"] + (13 - card["maxLevel"])
            o_deck_1.append((card["id"], card_level))
            o_cards_avg_1 += card_level / 8

        for card in battle["opponent"][1]["cards"]:
        
            card_level = card["level"] + (13 - card["maxLevel"])
            o_deck_2.append((card["id"], card_level))
            o_cards_avg_2 += card_level / 8

        m_deck_1.sort()
        m_deck_2.sort()
        o_deck_1.sort()
        o_deck_2.sort()

        del battle["opponent"][0]["cards"]
        del battle["opponent"][1]["cards"]
        del battle["team"][0]["cards"]
        del battle["team"][1]["cards"]
        

        if battle["team"][0]["crowns"] > battle["opponent"][0]["crowns"]:
            m_win = True

        elif battle["team"][0]["crowns"] < battle["opponent"][0]["crowns"]:
            m_win = False

        else:
            m_win = 0

        battle["team"][0].update({"mDeck":m_deck_1, "mCardsAvg":m_cards_avg_1, "mPB":m_PB_1, "mKingLevel":m_king_level_1, "mWin":m_win})
        battle["team"][1].update({"mDeck":m_deck_2, "mCardsAvg":m_cards_avg_2, "mPB":m_PB_2, "mKingLevel":m_king_level_2, "mWin":m_win})
        battle["opponent"][0].update({"oDeck":o_deck_1, "oCardsAvg":o_cards_avg_1, "oPB":o_PB_1, "oKingLevel":o_king_level_1})
        battle["opponent"][1].update({"oDeck":o_deck_2, "oCardsAvg":o_cards_avg_2, "oPB":o_PB_2, "oKingLevel":o_king_level_2})


        battle["parsed"] = True

        return battle

    except:

        battle["parsed"] = False

        return battle

