import os
from parse_battles import parse_battles
from user_interraction import get_user_request
from draw_results import main_720x1080, cards_720x1080, most_used_decks_720x1080, faced_decks_720x1080

def main():

    try:
        battles, tag, period = get_user_request()
    except TypeError:
        return

    if battles == []:
        return

    result_dir = os.path.join(os.getcwd(), "results/")

    tag_dir = os.path.join(result_dir, tag+"/")
    if not os.path.isdir(tag_dir):
        os.mkdir(tag_dir)

    period_dir = os.path.join(tag_dir, period.replace(" ", "_")+"/")
    if not os.path.isdir(period_dir):
        os.mkdir(period_dir)

    parsed_battles_data = parse_battles(battles)

    main_720x1080(parsed_battles_data, tag, period, period_dir)
    cards_720x1080(parsed_battles_data, tag, period, period_dir)
    faced_decks_720x1080(parsed_battles_data, tag, period, period_dir)
    most_used_decks_720x1080(parsed_battles_data, tag, period, period_dir)


if __name__ == "__main__":

    main()


    