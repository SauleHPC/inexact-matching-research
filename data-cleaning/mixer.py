import random

def mix_characters(title_arr, character_swap_dictionary_arr, character_swap_odds):
    matched_dictionary = {}


    for i, title in enumerate(title_arr):
        rand_value = random.random()
        if rand_value <= character_swap_odds:
            character_swap_dictionary = random.choice(character_swap_dictionary_arr)
            
            new_title = ""
            for chara in title:
                if chara in character_swap_dictionary:
                    new_title += character_swap_dictionary[chara]
                elif(chara == ','):
                    pass
                else:
                    new_title += chara

        if new_title:
            matched_dictionary[new_title] = title
    return matched_dictionary
            

        