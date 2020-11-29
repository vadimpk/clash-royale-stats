def is_close_battle(team, opponent):

    if abs(team["crowns"] - opponent["crowns"]) == 1:

        if team["mWin"] == True:
            try:
                min_tower_hp_left = min(team["princessTowersHitPoints"])
            except:
                # if both princess towers are destroyed, KeyError will arise
                min_tower_hp_left = team["kingTowerHitPoints"]
        
        else:
            try:
                min_tower_hp_left = min(opponent["princessTowersHitPoints"])
            except:
                min_tower_hp_left = opponent["kingTowerHitPoints"]

        if min_tower_hp_left <= 400:
            return True


"""
-----------------------------------------------
GETTING BASE INFORMATION FROM ALL BATTLES GIVEN
-----------------------------------------------
"""
def parse_battles(battles):

    # list of what will be parsed
    battles_won = 0
    battles_lost = 0
    battles_draw = 0
    cards_played_against = {}
    cards_played = {}
    decks_played = {}
    decks_played_against = {}
    o_pb_list = []
    o_level_list = []
    pb_difference_results_list = []
    pb_difference_list = []
    battles_vs_higher_level = 0
    wins_vs_higher_level = 0
    battles_vs_lower_level = 0
    wins_vs_lower_level = 0
    battles_vs_higher_pb = 0
    wins_vs_higher_pb = 0
    battles_vs_lower_pb = 0
    wins_vs_lower_pb = 0
    battles_vs_higher_deck_level = 0
    wins_vs_higher_deck_level = 0
    battles_vs_lower_deck_level = 0
    wins_vs_lower_deck_level = 0
    win_streak_ids = []
    win_streak = []
    longest_win_streak = 0
    longest_lose_streak = 0
    win_count = 0
    lose_count = 0
    win_close_matches = 0
    lose_close_matches = 0

    # --------------------------------------
    # CALCUALTING WIN STREAK
    # --------------------------------------

    # getting last 5 battles from list 
    # if there are less than 5 battles, getting all that exist (1-4)
    for i in range(5):
        if (len(battles) - i) > 0:
            if battles[-1-i]["team"][0]["mWin"] == True:
                # if won
                win_streak.append("W")

            elif battles[-1-i]["team"][0]["mWin"] == False:
                # if lost
                win_streak.append("L")

            else:
                # if draw
                win_streak.append("D")

    for battle in battles:

        team = battle["team"][0]
        opponent = battle["opponent"][0]
        
        # --------------------------------------
        # PARSING INFO BASED ON LEVEL AND PB
        # --------------------------------------

        o_pb_list.append(opponent["oPB"]) # list of all opponents' pb
        o_level_list.append(opponent["oKingLevel"]) # list of all opponents' king level
        pb_difference_list.append(team["mPB"] - opponent["oPB"]) # list of all differences in pb
        # type: (pb_difference(number), True/False(win/lose))
        pb_difference_results_list.append((team["mPB"] - opponent["oPB"], team["mWin"]))

        if team["mWin"] == True:
            # if won
            battles_won += 1 

            # calculating longest win & lose streaks
            win_count += 1
            if lose_count > longest_lose_streak:
                longest_lose_streak = lose_count
            lose_count = 0

            if team["mKingLevel"] > opponent["oKingLevel"]:
                battles_vs_lower_level += 1
                wins_vs_lower_level += 1
            elif team["mKingLevel"] < opponent["oKingLevel"]:
                battles_vs_higher_level += 1
                wins_vs_higher_level += 1
            
            if team["mPB"] > opponent["oPB"]:
                battles_vs_lower_pb += 1
                wins_vs_lower_pb += 1
            else:
                battles_vs_higher_pb += 1
                wins_vs_higher_pb += 1

            if is_close_battle(team, opponent):
                win_close_matches += 1

        else:
            if team["mKingLevel"] > opponent["oKingLevel"]:
                battles_vs_lower_level += 1
            elif team["mKingLevel"] < opponent["oKingLevel"]:
                battles_vs_higher_level += 1
            
            if team["mPB"] > opponent["oPB"]:
                battles_vs_lower_pb += 1
            else:
                battles_vs_higher_pb += 1

            if is_close_battle(team, opponent):
                lose_close_matches += 1

            if team["mWin"] == False:
                # if lost
                battles_lost += 1
                # calculating longest win & lose streaks
                lose_count += 1
                if win_count > longest_win_streak:
                    longest_win_streak = win_count
                win_count = 0
                    
            else:
                # if draw
                battles_draw += 1

        # --------------------------------------
        # GETTING INFO FROM OPPONENT'S DECK
        # --------------------------------------

        o_deck_name = ""
        m_deck_name = ""
        o_deck = []
        m_deck = []
        m_deck_level = 0
        o_deck_level = 0

        # sorting to make every deck with the same cards look similar 
        # no matter in what order cards are placed
        # it's needed to make the same name (id) for each similar deck
        opponent["oDeck"].sort()

        for card in opponent["oDeck"]:

            o_deck_name += str(card[0]) # that's why we sorted
            o_deck.append(card[0]) # list of card ids'
            o_deck_level += card[1] # summed level of all cards in deck

            # adding cards to cards played against

            # if it's the first time this card being faced - add a new dictionary
            if card[0] not in cards_played_against:
                cards_played_against[card[0]] = {
                    "games": 0,
                    "wins": 0,
                }

            # then add +1 game and +1 win (if won) for this card
            cards_played_against[card[0]]["games"] += 1
            
            if team["mWin"] == True:
                cards_played_against[card[0]]["wins"] += 1

        # adding deck to decks played against
        if o_deck_name not in decks_played_against:
            decks_played_against[o_deck_name] = {
                "deck": o_deck,
                "games": 0,
                "wins": 0,
            }

        decks_played_against[o_deck_name]["games"] += 1
            
        if team["mWin"] == True:
            decks_played_against[o_deck_name]["wins"] += 1

        # --------------------------------------
        # GETTING INFO FROM MATE'S DECK
        # --------------------------------------

        team["mDeck"].sort()
        for card in team["mDeck"]:

            m_deck_name += str(card[0])
            m_deck.append(card[0])
            m_deck_level += card[1]

            # adding cards to cards played with
            if card[0] not in cards_played:
                cards_played[card[0]] = {
                    "games": 0,
                    "wins": 0,
                }

            cards_played[card[0]]["games"] += 1
            
            if team["mWin"] == True:
                cards_played[card[0]]["wins"] += 1

        # adding deck to decks played with
        if m_deck_name not in decks_played:
            decks_played[m_deck_name] = {
                "deck": m_deck,
                "games": 0,
                "wins": 0,
                "faced_decks": {}
            }
        
        decks_played[m_deck_name]["games"] += 1

        # for every deck played with there is an individual dict of faced decks 
        # it's not used for now in the product, but has a great potential
        if o_deck_name not in decks_played[m_deck_name]["faced_decks"]:
            decks_played[m_deck_name]["faced_decks"][o_deck_name] = {
                "games": 0,
                "wins": 0,
            }

        decks_played[m_deck_name]["faced_decks"][o_deck_name]["games"] += 1
            
        if team["mWin"] == True:
            decks_played[m_deck_name]["wins"] += 1
            decks_played[m_deck_name]["faced_decks"][o_deck_name]["wins"] += 1

        # --------------------------------------
        # COMPARING OPPONENT'S AND MATE'S DECKS
        # --------------------------------------

        o_deck_level = o_deck_level / 8
        m_deck_level = m_deck_level / 8

        if o_deck_level > m_deck_level:
            battles_vs_higher_deck_level += 1

            if team["mWin"] == True:
                wins_vs_higher_deck_level += 1

        elif o_deck_level < m_deck_level:
            battles_vs_lower_deck_level += 1

            if team["mWin"] == True:
                wins_vs_lower_deck_level += 1

    # checking the last battle on longest win & lose streak
    if lose_count > longest_lose_streak:
        longest_lose_streak = lose_count
    if win_count > longest_win_streak:
        longest_win_streak = win_count

    name = team["name"] # getting last used name from last battle to use it in image drawing

    percents_list =  [
            battles_vs_higher_pb,
            wins_vs_higher_pb,
            battles_vs_lower_pb,
            wins_vs_lower_pb,
            battles_vs_higher_level,
            wins_vs_higher_level,
            battles_vs_lower_level,
            wins_vs_lower_level,
            battles_vs_higher_deck_level,
            wins_vs_higher_deck_level,
            battles_vs_lower_deck_level,
            wins_vs_lower_deck_level,
        ]

    # --------------------------------------
    # ADJUSTING PERCENTS INFORMATION
    # --------------------------------------

    minimum_battles_count = len(battles) * 0.05

    # case 2
    if battles_vs_higher_level < minimum_battles_count and battles_vs_higher_deck_level < minimum_battles_count:
        del percents_list[4:6]
        del percents_list[6:8]
        percents_list.append(win_close_matches)
        percents_list.append(lose_close_matches)
        percents_list.append(longest_win_streak)
        percents_list.append(longest_lose_streak)
        case = 2
    # case 3
    elif battles_vs_higher_level < minimum_battles_count:
        del percents_list[4:6]
        percents_list.append(win_close_matches)
        percents_list.append(lose_close_matches)
        case = 3
    # case 3
    elif battles_vs_higher_deck_level < minimum_battles_count:
        del percents_list[8:10]
        percents_list.append(win_close_matches)
        percents_list.append(lose_close_matches)
        case = 4
    # case 1
    else:
        case = 1
        
    # information for drawing file
    context = {
        "case": case,
        "name": name,
        "total_battles": len(battles),
        "wins": battles_won,
        "loses": battles_lost,
        "draws": battles_draw,
        "cards_played_against": cards_played_against,
        "cards_played": cards_played,
        "decks_played": decks_played,
        "decks_played_against": decks_played_against,
        "o_pb_list": o_pb_list,
        "o_level_list": o_level_list,
        "pb_difference_results_list": pb_difference_results_list,
        "pb_difference_list": pb_difference_list,
        "win_streak": win_streak,
        "percents": percents_list
    }

    return context


"""
----------------------------------------------------
CALCULATING WIN & PLAY PERCENTAGES FOR CARDS & DECKS
   (can be used only after all battles are parsed)
----------------------------------------------------
"""
def calculate_cards_percentages(cards, total_battles):

    cards_win_percentages = {}
    cards_play_percentages = {}

    for card in cards:

        win_percentage = round(cards[card]["wins"] / cards[card]["games"] * 100)
        play_percentage = round(cards[card]["games"] / total_battles * 100)

        cards[card]["win_percentage"] = win_percentage
        cards[card]["play_percentage"] = play_percentage
        cards_play_percentages[card] = play_percentage

        if play_percentage > 4:
            cards_win_percentages[card] = win_percentage
            
    cards_best_play_percentages = {k: v for k, v in sorted(cards_play_percentages.items(), key=lambda item: item[1], reverse=True)}
    cards_best_win_percentages = {k: v for k, v in sorted(cards_win_percentages.items(), key=lambda item: item[1], reverse=True)}
    cards_worst_win_percentages = {k: v for k, v in sorted(cards_win_percentages.items(), key=lambda item: item[1])}

    return cards_best_play_percentages, cards_best_win_percentages, cards_worst_win_percentages, cards

def calculate_decks_percentages(decks, total_battles):

    decks_count = 0
    decks_play_percentages = {}
    decks_win_percentages = {}

    for deck in decks:

        if decks[deck]["games"] > 1:

            decks_count += 1

            win_percentage = round(decks[deck]["wins"] / decks[deck]["games"] * 100)
            play_percentage = round(decks[deck]["games"] / total_battles * 100, 1)

            decks[deck]["win_percentage"] = win_percentage
            decks[deck]["play_percentage"] = play_percentage

            if play_percentage > 0.5:
                decks_play_percentages[deck] = play_percentage
                decks_win_percentages[deck] = win_percentage

    decks_play_percentages = {k: v for k, v in sorted(decks_play_percentages.items(), key=lambda item: item[1], reverse=True)}
    decks_best_win_percentages = {k: v for k, v in sorted(decks_win_percentages.items(), key=lambda item: item[1], reverse=True)}
    decks_worst_win_percentages = {k: v for k, v in sorted(decks_win_percentages.items(), key=lambda item: item[1])}

    return decks_play_percentages, decks_best_win_percentages, decks_worst_win_percentages, decks

def calculate_used_decks_percentages(decks, total_battles):

    decks_play_percentages = {}

    for deck in decks:

        win_percentage = round(decks[deck]["wins"] / decks[deck]["games"] * 100)
        play_percentage = round(decks[deck]["games"] / total_battles * 100, 1)

        decks[deck]["win_percentage"] = win_percentage
        decks[deck]["play_percentage"] = play_percentage    

        if play_percentage > 1:
            decks_play_percentages[deck] = play_percentage

    decks_play_percentages = {k: v for k, v in sorted(decks_play_percentages.items(), key=lambda item: item[1], reverse=True)}

    return decks_play_percentages, decks
