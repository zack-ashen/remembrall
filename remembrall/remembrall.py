"""
Remembrall
Author: Zachary Ashen
Date: June 15th 2020
Description: A CLI flashcard utility for studying sets.
Can import Quizlet sets or make new sets to study from.
Contact: zachary.h.a@gmail.com
"""

import os
from pathlib import Path
from time import sleep
import json
import sys

from PyInquirer import prompt
from pyfiglet import Figlet
import argparse
import keyboard
import getch

from set import Set, Card
import consts
import ui


def save_set(set_list):
    set_dict = {}

    for set in set_list:
        set_dict[set.get_title()] = set.to_list()

    set_file = open(consts.PATH_TO_SETS + '/sets.json', 'w')
    json.dump(set_dict, set_file)


def retrieve_sets():
    sets_file = open(consts.PATH_TO_SETS + '/sets.json', 'r')

    set_dict = json.load(sets_file)
    set_list = []
    for set_title in set_dict:
        cards = []
        for card in set_dict[set_title]:
            new_card = Card(card[0], card[1])
            cards.append(new_card)

        current_set = Set(set_title, cards)
        set_list.append(current_set)

    return set_list


def get_set_titles():
    set_list = retrieve_sets()

    set_titles = []
    for set in set_list:
        set_titles.append(set.get_title())

    return set_titles


def make_set_title():
    set_title_prompt = {
        'type': 'input',
        'name': 'set_title',
        'message': 'What should the name of the set be?',
        'type': 'input'
    }
    set_title_input = prompt(set_title_prompt)
    return set_title_input['set_title']


def make_cards():
    continue_adding_cards = True
    card_list = []
    while continue_adding_cards:
        ui.print_dividing_line()

        add_card_prompt = [{
            'type': 'input',
            'name': 'card_term',
            'message': 'What should be the card term? (Enter \'-\' to finish)',
        },
            {
                'type': 'input',
                'name': 'card_definition',
                'message': 'What should the card definition be? (Enter \'-\' to finish)'
            }]
        card_details = prompt(add_card_prompt)

        card_term = card_details['card_term']
        card_definition = card_details['card_definition']
        if card_term == '-' or card_definition == '-':
            continue_adding_cards = False
        else:
            new_card = Card(card_term, card_definition)
            card_list.append(new_card)
    return card_list


def add_set():
    # get a title for the set
    set_title = make_set_title()

    # add cards to set
    card_list = make_cards()

    return Set(set_title, card_list)


def edit_set(set_to_edit):
    return set


def study_set(set_to_study, card_counter=0, previous_cards=[], prev_card=False, starred=False):
    # Display Card
    set_length = len(set_to_study)

    if prev_card:
        ui.study_prompt(previous_cards[card_counter], card_counter, set_length)
        cur_card = previous_cards[card_counter]
    elif starred:
        set_length = len(set_to_study.get_starred_cards())

        cur_card = set_to_study.get_starred_cards()[card_counter]
        ui.study_prompt(cur_card, card_counter, set_length)
    else:
        cur_card = set_to_study.get_cards()[card_counter]
        ui.study_prompt(cur_card, card_counter, set_length)

    # Handle Key Presses
    term_showing = True
    while True:
        choice = getch.getch()
        if choice == ' ':
            if term_showing:
                ui.study_prompt(cur_card, card_counter, set_to_study, set_length, show_definition=True)
                term_showing = False
            else:
                ui.study_prompt(cur_card, card_counter, set_length)
                term_showing = True
        elif choice == 'q':
            set_view()
        elif choice == 's':
            if cur_card.get_is_starred():
                cur_card.set_is_starred(False)
                study_set(set_to_study, card_counter=card_counter, previous_cards=previous_cards, starred=starred)
            else:
                cur_card.set_is_starred(True)
                study_set(set_to_study, card_counter=card_counter, previous_cards=previous_cards, starred=starred)
        elif choice == 'h' and card_counter > 0:
            study_set(set_to_study, card_counter=card_counter - 1, previous_cards=previous_cards, prev_card=True, starred=starred)
        elif choice == 'l' and card_counter != set_length-1:
            if not prev_card:
                previous_cards.append(cur_card)
            study_set(set_to_study, card_counter=card_counter + 1, previous_cards=previous_cards, starred=starred)
        elif card_counter == set_length-1:
            finished_studying_message = {
                'type': 'list',
                'name': 'post_studying_choice',
                'message': consts.FINISHED_STUDYING,
                'choices': [consts.STUDY_AGAIN, consts.STUDY_RESHUFFLE, consts.STUDY_STARRED, consts.GO_BACK]
            }

            try:
                finished_studying_choice = prompt(finished_studying_message)['post_studying_choice']
            except KeyError:
                raise SystemExit

            if finished_studying_choice == consts.STUDY_AGAIN:
                study_set(set_to_study, card_counter=0)
            elif finished_studying_choice == consts.STUDY_RESHUFFLE:
                set_to_study.shuffle()
                study_set(set_to_study, card_counter=0)
            elif finished_studying_choice == consts.STUDY_STARRED:
                study_set(set_to_study, card_counter=0, starred=True)
            elif finished_studying_choice == consts.GO_BACK:
                set_view()


def set_view():

    try:
        set_choices = get_set_titles()

        set_choices.append(consts.ADD_SET)
        set_choices.append(consts.EXIT)
    except json.decoder.JSONDecodeError:
        set_choices = [consts.ADD_SET, consts.EXIT]
    except FileNotFoundError:
        print(consts.RED, 'It looks like you haven\'t initialized a file to store your sets!' \
                          ' To do this run \'remembrall --init\'.'.center(consts.WIDTH))
        raise SystemExit

    set_options_prompt = {
        'type': 'list',
        'name': 'option_selection',
        'message': consts.INITIAL_PROMPT,
        'choices': set_choices
    }

    try:
        set_options = prompt(set_options_prompt)['option_selection']
    except KeyError:
        raise SystemExit

    if set_options == consts.ADD_SET:
        new_set = add_set()
        try:
            set_list = retrieve_sets()
            set_list.append(new_set)
            save_set(set_list)
            set_view()
        except:
            set_list = [new_set]
            save_set(set_list)
            set_view()
    elif set_options == consts.EXIT:
        raise SystemExit
    else:
        selected_set_prompt = {
            'type': 'list',
            'name': 'set_selection_choice',
            'message': consts.GENERIC_PROMPT,
            'choices': [consts.STUDY_SET, consts.EDIT_SET, consts.GO_BACK]
        }

        try:
            selected_set_choice = prompt(selected_set_prompt)['set_selection_choice']
        except KeyError:
            raise SystemExit

        index_of_set = set_choices.index(set_options)

        if selected_set_choice == consts.EDIT_SET:
            set_list = retrieve_sets()
            set_list[index_of_set] = edit_set(set_list[index_of_set])
        elif selected_set_choice == consts.STUDY_SET:
            set_list = retrieve_sets()
            set_list[index_of_set].shuffle()
            study_set(set_list[index_of_set])
        elif selected_set_choice == consts.GO_BACK:
            set_view()


def display_intro_animation():
    title = 'remembrall...'
    fig = Figlet(font='stop', justify='center', width=consts.WIDTH)

    print(consts.CYAN_BOLD)

    # animate welcome text
    title_accumulator = ''
    for character in title:
        sleep(0.1)
        os.system('clear')
        title_accumulator += character

        # center text vertically
        print('\n' * round(consts.HEIGHT / 5))
        print(fig.renderText(title_accumulator))


def initialize():
    # initialize folder in .config folder to store all of the sets in json
    print('This will make a directory at the location ~/.config/remembrall and place a file ' \
          'in it to store your sets.')
    sleep(1)

    if os.path.isdir(consts.PATH_TO_SETS):
        print(consts.RED_BOLD, 'It seems like you have already initialized a storage file!')
    else:
        os.system('mkdir -p ' + consts.PATH_TO_SETS)
        os.system('touch ' + consts.PATH_TO_SETS + '/sets.json')


def handle_arguments():
    args = argparse.ArgumentParser(description='A simple cli notecard application for studying...')
    args.add_argument('--init', help='initialize new file for storing sets.', action='store_true')
    args.add_argument('--delete', '-d', help='delete a set. Lists all the possible sets you can delete and allows for '
                                             'selection.', action='store_true')
    args.add_argument('--add', '-a', help='create a set', action='store_true')
    args.add_argument('--quick', '-q', help='skip intro animation...quickly start studying', action='store_true')
    args.add_argument('--import', '-i', help='import a quizlet set')

    parser = args.parse_args()
    if parser.init:
        initialize()
    elif parser.quick:
        set_view()
    else:
        display_intro_animation()
        set_view()


def main():
    handle_arguments()


if __name__ == '__main__':
    main()
