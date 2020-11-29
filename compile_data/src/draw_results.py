from PIL import Image, ImageDraw, ImageFont
import os
import statistics
import operator
import json

from parse_battles import calculate_cards_percentages, calculate_decks_percentages, calculate_used_decks_percentages

src_dir = os.getcwd()
base_dir = os.path.normpath(src_dir + os.sep)
samples_folder = os.path.join(base_dir, "data/samples/")
cards_folder = os.path.join(base_dir, "data/cards/")
smaller_cards_folder = os.path.join(base_dir, "data/smaller_cards/")

colors = {
    "green": (27,181,14),
    "red": (181,14,14),
    "brown": (176,116,4),
    "white": (255,255,255),
    "light-green": (90,220,80),
    "light-red": (228,65,65)
}

# fonts
font_24 = ImageFont.truetype("/Library/Fonts/Supercell.ttf", 24, encoding='UTF-8')
font_24_noto = ImageFont.truetype("/Library/Fonts/NotoSans-Bold.ttf", 24, encoding='UTF-8')
font_21 = ImageFont.truetype("/Library/Fonts/Supercell.ttf", 21, encoding='UTF-8')
font_18 = ImageFont.truetype("/Library/Fonts/Supercell.ttf", 18, encoding='UTF-8')

additionals_path = os.path.join(base_dir, 'data/additionals.json')
with open(additionals_path, 'r') as outfile:
    data = json.load(outfile)

    card_names = data["card_names"]
    card_types = data["card_types"]
    number_sizes = data["number_sizes"]
    win_conditions = data["win_conditions"]

def draw_name(img, name):

    draw_name = ImageDraw.Draw(img)
    draw_name_color = colors["white"]

    # if there is non-English letters in name, font will be changed to international
    try:
        name.encode(encoding='utf-8').decode('ascii')
        font = font_24
    except UnicodeDecodeError:
        font = font_24_noto

    draw_name.text((113,122), name, font=font, fill=draw_name_color)

def draw_period(img, period):

    draw_period = ImageDraw.Draw(img)
    draw_period_color = colors["white"]
    draw_period.text((566,129), period, font=font_18, fill=draw_period_color)

def define_color_of_win_percentage(percents):
    
    if isinstance(percents, str):
        percents = float(percents)

    if percents <= 0:
        color = colors["white"]
    elif percents <= 25:
        color = colors["red"]
    elif percents <= 45:
        color = colors["light-red"]
    elif percents < 55:
        color = colors["white"]
    elif percents < 75:
        color = colors["light-green"]
    else: 
        color = colors["green"]

    return color

"""
--------------------------------------------------
                MAIN IMAGE DRAWING
--------------------------------------------------
"""

def main_720x1080(data, tag, period, result_folder):

    # I added the part with cases after cleaning and documenting the code, 
    # so, to understand better what it is check parse_battles.py 
    # ADJUSTING PERCENTS INFORMATION section in the end

    sample_name = "main_720x1080_" + str(data["case"])

    sample = os.path.join(samples_folder, sample_name + ".png")
    img = Image.open(sample)

    draw_name(img, data["name"])
    draw_period(img, period)

    # ------------------------------------
    # DRAWING RECORD
    # ------------------------------------
    x_cord = 685
    y_cord = 235

    # how it should look: wins - draws - loses
    # we start with loses and take every number (reversed) and draw it.
    # then draw spaces, then draws, again spaces and finally wins
    record_values = [
        reversed(str(data["loses"])),
        reversed(str(data["draws"])),
        reversed(str(data["wins"]))
        ]
    for index, value in enumerate(record_values):
        for number in value:

            # every number has different width, so we need to
            # retreat different amount of pixels after every number
            draw_number_size = number_sizes[number]
            if index == 0:
                draw_number_color = colors["red"]
            elif index == 1:
                draw_number_color = colors["white"]
            else:
                draw_number_color = colors["green"]
            x_cord -= draw_number_size

            draw_number = ImageDraw.Draw(img)
            draw_number.text((x_cord,y_cord), number, font=font_24, fill=draw_number_color)

        # do not draw last spaces
        if index != 2:

            draw_spaces_color = colors["brown"]
            x_cord -= 29

            draw_spaces = ImageDraw.Draw(img)
            draw_spaces.text((x_cord,y_cord), " - ", font=font_24, fill=draw_spaces_color)

    # ------------------------------------
    # DRAWING WIN STREAK
    # ------------------------------------
    x_cord = 685
    y_cord = 295

    win_streak_colors = {
        "W": (27,181,14),
        "L": (181,14,14),
        "D": (255,255,255),
    }

    win_streak_sizes = {
        "W": 32,
        "L": 19,
        "D": 26,
    }

    for index, value in enumerate(reversed(data["win_streak"])):

        draw_letter_color = win_streak_colors[value]
        draw_letter_size = win_streak_sizes[value]
        x_cord -= draw_letter_size

        draw_letter = ImageDraw.Draw(img)
        draw_letter.text((x_cord,y_cord), value, font=font_24, fill=draw_letter_color)

        # do not draw last spaces
        if (index + 1) != len(data["win_streak"]):

            draw_spaces_color = colors["brown"]
            x_cord -= 29

            draw_spaces = ImageDraw.Draw(img)
            draw_spaces.text((x_cord,y_cord), " - ", font=font_24, fill=draw_spaces_color)

    # ------------------------------------
    # DRAWING TOTAL WIN PERCENTAGE
    # ------------------------------------

    win_percent = round(data["wins"] / data["total_battles"] * 100)

    text = str(win_percent) + " %"
    draw_win_percent_color = define_color_of_win_percentage(win_percent)

    draw_win_percent = ImageDraw.Draw(img)
    draw_win_percent.text((603, 355), text, font=font_24, fill=draw_win_percent_color) 

    # ------------------------------------
    # DRAWING THE OTHER PERCENTAGES
    # ------------------------------------

    x_cord = 608
    y_cord = 415
    step = 53
    
    # all the percentages go in pairs (facing - winning)
    # so for one iteration we will draw one pair (facing - winning)
    # total iterations (pairs) - 6 
    for i in range(0, 12, 2):

        
        facing_percent = round(data["percents"][i] / data["total_battles"] * 100)
        try:
            winning_percent = round(data["percents"][i+1] / data["percents"][i] * 100)
        except ZeroDivisionError:
            winning_percent = 0

        # draw facing percentage
        text = str(facing_percent) + " %"
        draw_facing_percent_color = colors["white"]
        draw_font = font_21

        if (data["case"] == 2 and i == 8) or ( (data["case"] == 3 or data["case"] == 4) and i == 10):
            total = data["percents"][i] + data["percents"][i+1]
            if total != 0:

                facing_percent = round(data["percents"][i] / total * 100)
                draw_facing_percent_color = define_color_of_win_percentage(facing_percent)
                text = str(facing_percent) + " %"
            else:
                text = "0 %"

        if data["case"] == 2 and i == 10:
            facing_percent = data["percents"][i]
            draw_facing_percent_color = colors["green"]
            draw_font = font_24
            text = str(facing_percent)

        draw_facing_percent = ImageDraw.Draw(img)
        draw_facing_percent.text((x_cord, y_cord), text, font=draw_font, fill=draw_facing_percent_color)

        y_cord += step # then make 1 step down

        # draw winning percentage
        text = str(winning_percent) + " %"
        draw_winning_percent_color = define_color_of_win_percentage(winning_percent)

        if (data["case"] == 2 and i == 8) or ( (data["case"] == 3 or data["case"] == 4) and i == 10):
            total = data["percents"][i] + data["percents"][i+1]
            if total != 0:
    
                winning_percent = round(data["percents"][i+1] / total * 100)
                draw_winning_percent_color = define_color_of_win_percentage(winning_percent)
                text = str(winning_percent) + " %"
            else:
                draw_winning_percent_color = colors["white"]
                text = "0 %"

        if data["case"] == 2 and i == 10:
            winning_percent = data["percents"][i+1]
            draw_winning_percent_color = colors["red"]
            draw_font = font_24
            text = str(winning_percent)

        draw_winning_percent = ImageDraw.Draw(img)
        draw_winning_percent.text((x_cord, y_cord), text, font=draw_font, fill=draw_winning_percent_color)

        y_cord += step # 1 step down again

    file_name = str(tag)+ ".png"
    img.save(os.path.join(result_folder, file_name))

"""
---------------------------------------------------
                CARDS IMAGE DRAWING
---------------------------------------------------
"""

def cards_720x1080(data, tag, period, result_folder):

    # there will be 4 images compiled
    #   
    #   1. most faced cards
    #   2. best win percentage cards
    #   3. worst win percentage cards
    #   4. win percentage against win conditions

    cards_best_play_percentages, cards_best_win_percentages, cards_worst_win_percentages, cards_played_against = calculate_cards_percentages(data["cards_played_against"], data["total_battles"])

    for i in range(4):

        # first image (most faced cards)
        sample = os.path.join(samples_folder, "most_faced_cards_720x1080.png")
        file_name = str(tag)+ "_most_faced_cards.png"
        query = cards_best_play_percentages

        if i == 1:

            # second image (best win percentage cards)
            sample = os.path.join(samples_folder, "best_win_cards_720x1080.png")
            file_name = str(tag)+ "_best_win_cards.png"
            query = cards_best_win_percentages
        
        elif i == 2:
            
            # third image (worst win percentage cards)
            sample = os.path.join(samples_folder, "worst_win_cards_720x1080.png")
            file_name = str(tag)+ "_worst_win_cards.png"
            query = cards_worst_win_percentages

        elif i == 3:
            
            # fourth image (worst win percentage cards)
            sample = os.path.join(samples_folder, "win_percentage_against_win_conditions.png")
            file_name = str(tag)+ "_win_conditions.png"
            query = win_conditions

        img = Image.open(sample)

        draw_name(img, data["name"])
        draw_period(img, period)

        keys_view = query.keys()
        key_iterator = iter(keys_view)
    
        for j in range(2): 

            # left column
            img_x_cord = 22
            win_percent_x_cord = 157
            play_percent_x_cord = 281

            if j == 1:

                # right column
                img_x_cord = 384
                win_percent_x_cord = 519
                play_percent_x_cord = 643

            # row
            img_y_cord = 274
            percents_y_cord = 315
            y_cord_difference = 128

            for card in range(6):

                card_id = str(next(key_iterator))

                # draw image
                card_filename = card_names[card_id] + ".png"
                card_image = Image.open(os.path.join(cards_folder, card_filename))

                mask_filename = card_types[card_id] + "_mask.png"
                mask = Image.open(os.path.join(samples_folder, mask_filename))

                img.paste(card_image, (img_x_cord, img_y_cord))
                img.paste(mask, (img_x_cord, img_y_cord), mask)

                img_y_cord += y_cord_difference

                # draw win percentage
                percents = int(cards_played_against[int(card_id)]["win_percentage"])
                text = str(percents) + " %"
                draw_percents_color = define_color_of_win_percentage(percents)

                draw_percents = ImageDraw.Draw(img)
                draw_percents.text((win_percent_x_cord,percents_y_cord), text, font=font_21, fill=draw_percents_color)

                # draw play percentage
                percents = int(cards_played_against[int(card_id)]["play_percentage"])
                text = str(percents) + " %"
                draw_percents_color = colors["white"]

                draw_percents = ImageDraw.Draw(img)
                draw_percents.text((play_percent_x_cord,percents_y_cord), text, font=font_21, fill=draw_percents_color)

                percents_y_cord += y_cord_difference # make a step down

            img.save(os.path.join(result_folder, file_name))

"""
---------------------------------------------------------
                FACED DECKS IMAGE DRAWING
---------------------------------------------------------
"""

def faced_decks_720x1080(data, tag, period, result_folder):

    # only decks that were played against more than 0.5 % from all battles
    decks_play_percentages, decks_best_win_percentages, decks_worst_win_percentages, decks = calculate_decks_percentages(data["decks_played_against"], data["total_battles"])
    decks_count = len(decks_play_percentages)

    if decks_count == 0:
        # if no such decks - skip
        # it's common for midladder or for low amount of battles
        return

    # ------------------------------------
    # DRAWING MOST FACED DECKS
    # ------------------------------------

    elif decks_count > 8:

        sample = os.path.join(samples_folder, "most_faced_decks_720x1080.png")
        img = Image.open(sample)

        draw_name(img, data["name"])
        draw_period(img, period)

        # coords
        img_y_cord = 311
        win_percent_x_cord = 530
        play_percent_x_cord = 633
        percents_y_cord = 331

        keys_view = decks_play_percentages.keys()
        key_iterator = iter(keys_view)

        # total 8 decks (can't place more on one image)
        for i in range(8):

            deck_id = str(next(key_iterator))
            img_x_cord = 22

            # draw every card (8 in total) in a row
            for card in decks[deck_id]["deck"]:
                
                # draw an image (smaller one)
                card_filename = card_names[str(card)] + ".png"
                card_image =  Image.open(os.path.join(smaller_cards_folder, card_filename))

                mask_filename = "small_" + card_types[str(card)] + "_mask.png"
                mask = Image.open(os.path.join(samples_folder, mask_filename))

                img.paste(card_image, (img_x_cord, img_y_cord))
                img.paste(mask, (img_x_cord, img_y_cord), mask)
                
                img_x_cord += 60 # make 1 step right for next image (8 in total)
        
            img_y_cord += 91 # make 1 step down for next row

            # draw win percentage
            percents = decks[deck_id]["win_percentage"]
            text = str(percents) + " %"
            draw_percents_color = define_color_of_win_percentage(percents)

            draw_percents = ImageDraw.Draw(img)
            draw_percents.text((win_percent_x_cord,percents_y_cord), text, font=font_18, fill=draw_percents_color)

            # draw play percentage
            percents = decks[deck_id]["play_percentage"]
            text = str(percents) + " %"
            draw_percents_color = colors["white"]

            draw_percents = ImageDraw.Draw(img)
            draw_percents.text((play_percent_x_cord,percents_y_cord), text, font=font_18, fill=draw_percents_color)

            percents_y_cord += 91 # make a step for next row

        file_name = str(tag)+ "_most_faced_decks.png"
        img.save(os.path.join(result_folder, file_name))
    
    # ------------------------------------
    # DRAWING BEST & WORST WIN DECKS
    # ------------------------------------

    if decks_count > 16: # needs to be enough for 2 images

        for i in range(2):
            
            # best win percentage decks
            query = decks_best_win_percentages
            sample = os.path.join(samples_folder, "best_win_decks_720x1080.png")
            img = Image.open(sample)
            file_name = str(tag)+ "_best_win_decks.png"
            
            if i == 1:
                
                # worst win percentage decks
                query = decks_worst_win_percentages
                sample2 = os.path.join(samples_folder, "worst_win_decks_720x1080.png")
                img = Image.open(sample2)
                file_name = str(tag)+ "_worst_win_decks.png"

            draw_name(img, data["name"])
            draw_period(img, period)

            # coords
            img_y_cord = 311
            win_percent_x_cord = 530
            play_percent_x_cord = 633
            percents_y_cord = 331

            keys_view = query.keys()
            key_iterator = iter(keys_view)

            # total 8 decks (can't place more on one image)
            for j in range(8):

                deck_id = str(next(key_iterator))
                img_x_cord = 22

                # draw every card (8 in total) in a row
                for card in decks[deck_id]["deck"]:
                    
                    # draw an image
                    card_filename = card_names[str(card)] + ".png"
                    card_image =  Image.open(os.path.join(smaller_cards_folder, card_filename))

                    mask_filename = "small_" + card_types[str(card)] + "_mask.png"
                    mask = Image.open(os.path.join(samples_folder, mask_filename))

                    img.paste(card_image, (img_x_cord, img_y_cord))
                    img.paste(mask, (img_x_cord, img_y_cord), mask)
                    
                    img_x_cord += 60
                
                img_y_cord += 91

                # draw win percentage
                percents = decks[deck_id]["win_percentage"]
                text = str(percents) + " %"
                draw_percents_color = define_color_of_win_percentage(percents)

                draw_percents = ImageDraw.Draw(img)
                draw_percents.text((win_percent_x_cord,percents_y_cord), text, font=font_18, fill=draw_percents_color)

                # draw play percentage
                percents = decks[deck_id]["play_percentage"]
                text = str(percents) + " %"
                draw_percents_color = colors["white"]

                draw_percents = ImageDraw.Draw(img)
                draw_percents.text((play_percent_x_cord,percents_y_cord), text, font=font_18, fill=draw_percents_color)
                
                percents_y_cord += 91 # make a step down for next row

            img.save(os.path.join(result_folder, file_name))

"""
--------------------------------------------------------
                USED DECKS IMAGE DRAWING
--------------------------------------------------------
"""

def most_used_decks_720x1080(data, tag, period, result_folder):

    # only decks with play percentage more than 1% of all battles
    # maximum decks: 3
    # minimum decks: 2
    decks_play_percentages, all_decks = calculate_used_decks_percentages(data["decks_played"], data["total_battles"])

    if len(decks_play_percentages) == 1:
        # if only 1 deck is used do nothing
        return

    else:
        # get list of decks that will be used in an image (2 or 3 decks)
        deck_count = 0
        decks = []

        for deck in decks_play_percentages:
            if deck_count < 3:
                decks.append(all_decks[deck])

            else:
                break
            deck_count += 1


    sample = os.path.join(samples_folder, "most_used_decks_720x1080.png")
    img = Image.open(sample)

    draw_name(img, data["name"])
    draw_period(img, period)
    
    deck_count = 0

    for deck in decks:

        card_count = 0
        deck_count += 1

        img_y_cord = 288
        img_x_cord = 30
        win_percent_x_cord = 460
        play_percent_x_cord = 574
        percents_y_cord = 384

        # playing with coordinates
        if deck_count == 2 and len(decks) == 2:
            img_y_cord = 593
            percents_y_cord = 689

        elif deck_count == 2 and len(decks) == 3:
            img_y_cord = 535
            percents_y_cord = 631
        
        elif deck_count == 3:
            img_y_cord = 782
            percents_y_cord = 878

        for card in deck["deck"]:

            card_count += 1

            # jumping into the next row (see image to understand better)
            if card_count == 5:

                img_y_cord += 113
                img_x_cord = 30

            # draw a card
            card_filename = card_names[str(card)] + ".png"
            card_image =  Image.open(os.path.join(cards_folder, card_filename))

            mask_filename = card_types[str(card)] + "_mask.png"
            mask = Image.open(os.path.join(samples_folder, mask_filename))

            img.paste(card_image, (img_x_cord, img_y_cord))
            img.paste(mask, (img_x_cord, img_y_cord), mask)

            img_x_cord += 95

        # draw win percentage
        percents = deck["win_percentage"]
        text = str(percents) + " %"
        draw_percents_color = define_color_of_win_percentage(percents)

        draw_percents = ImageDraw.Draw(img)
        draw_percents.text((win_percent_x_cord,percents_y_cord), text, font=font_24, fill=draw_percents_color)

        # draw play percentage
        percents = deck["play_percentage"]
        text = str(percents) + " %"
        draw_percents_color = colors["white"]

        draw_percents = ImageDraw.Draw(img)
        draw_percents.text((play_percent_x_cord,percents_y_cord), text, font=font_24, fill=draw_percents_color)

    file_name = str(tag)+ "_used_decks.png"
    img.save(os.path.join(result_folder, file_name))

        