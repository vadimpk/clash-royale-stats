import statistics
from connect_db import db
from get_data import get_player_cards


def get_sorted_cards_level(tag):

    cards = get_player_cards(tag)
    cards_level = []

    for card in cards:
        cards_level.append(int(cards[card][0]))

    sorted_cards_level = sorted(cards_level, reverse=True)

    return sorted_cards_level

def get_first_32_mean_cards_level(cards):

    query = cards[:32]

    return round(statistics.mean(query), 1)

def get_mean_cards_level(cards):

    return round(statistics.mean(cards), 1)

def print_mean_cards_level():
    players = db.players.find()
    for player in players:

        cards = get_sorted_cards_level(player["tag"])

        mean_32_cards = get_first_32_mean_cards_level(cards)
        mean_cards = get_mean_cards_level(cards)

        print(f"{player['tag']}:")
        print(f"\tmean level of all cards: {mean_cards}")
        print(f"\tmean level of first 32 cards: {mean_32_cards}")
        print()