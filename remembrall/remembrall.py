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
    try:
        sets_file = open(consts.PATH_TO_SETS + '/sets.json', 'r')
    except FileNotFoundError:
        print(consts.RED, 'It looks like you haven\'t initialized a file to store your sets!' \
                          ' To do this run \'remembrall --init\'.'.center(consts.WIDTH))
        raise SystemExit

    set_dict = json.load(sets_file)
    set_list = []
    for set_title in set_dict:
        cards = []
        for card in set_dict[set_title]:
            new_card = Card(card[0], card[1], is_starred=card[2])
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


def convert_quizlet(quizlet_file):
    try:
        set_list = retrieve_sets()
    except json.decoder.JSONDecodeError:
        set_list = []

    quizlet_file = quizlet_file.readlines()

    cards = []
    for term_index in range(len(quizlet_file)):
        card_str = quizlet_file[term_index]
        division_index = card_str.find('\t')

        term = card_str[:division_index]
        definition = card_str[division_index+1:-1]

        if definition == '':
            continue

        card = Card(term, definition)
        cards.append(card)

    set_title = make_set_title()
    quizlet_set = Set(set_title, cards)
    set_list.append(quizlet_set)
    save_set(set_list)

    print(consts.GREEN, 'Quizlet set converted!')


def make_set_title():
    set_title_prompt = {
        'type': 'input',
        'name': 'set_title',
        'message': 'What should the name of the set be?'
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


def delete_set(index_of_set):
    set_list = retrieve_sets()
    set_list.pop(index_of_set)
    save_set(set_list)


def edit_cards(set_to_edit):
    os.system('clear')
    
    print('Search for the card via its term to edit it.'.center(consts.WIDTH))

    i = 0
    for card in set_to_edit.get_cards():
        if i < consts.HEIGHT - 2:
            print((card.get_term()[:30] + '/' + card.get_definition()[:30]).center(consts.WIDTH))
        i += 1

    print('==> ', end='')

    try:
        search_string = input()
    except KeyboardInterrupt:
        raise SystemExit

    target_cards = set_to_edit.search(search_string)
    card_strings = [consts.SEARCH_AGAIN]
    for card in target_cards:
        card_strings.append((card.get_term()[:30] + '/' + card.get_definition()[:30]))

    search_prompt = {
        'type': 'list',
        'name': 'search_prompt_choice',
        'message': 'Select the card you want to edit:',
        'choices': card_strings
    }

    try:
        search_choice = prompt(search_prompt)['search_prompt_choice']
    except KeyError:
        raise SystemExit

    if search_choice == consts.SEARCH_AGAIN:
        edit_cards(set_to_edit)



def edit_set(set_to_edit, index_of_set):
    set_list = retrieve_sets()

    edit_set_prompt = {
        'type': 'list',
        'name': 'edit_set_choice',
        'message': consts.EDIT_SET_PROMPT,
        'choices': [consts.ADD_CARDS, consts.EDIT_CARDS, consts.RENAME_SET, consts.DELETE_SET, consts.GO_BACK]
    }

    try:
        edit_set_response = prompt(edit_set_prompt)['edit_set_choice']
    except KeyError:
        raise SystemExit

    if edit_set_response == consts.ADD_CARDS:
        new_cards = make_cards()
        set_to_edit.add_cards(new_cards)

        set_list[index_of_set] = set_to_edit
        save_set(set_list)
        edit_set(set_to_edit, index_of_set)
    elif edit_set_response == consts.EDIT_CARDS:
        edit_cards(set_to_edit)
    elif edit_set_response == consts.RENAME_SET:
        new_title = make_set_title()
        set_to_edit.set_title(new_title)

        set_list[index_of_set] = set_to_edit
        save_set(set_list)
        edit_set(set_to_edit, index_of_set)
    elif edit_set_response == consts.DELETE_SET:
        delete_set(index_of_set)
        set_view()
    elif edit_set_response == consts.GO_BACK:
        set_view()


def study_set(set_list, set_to_study, card_counter=0, previous_cards=[], prev_card=False, starred=False):
    # Display Card
    if starred:
        set_length = len(set_to_study.get_starred_cards())
        cur_card = set_to_study.get_starred_cards()[card_counter]
    else:
        set_length = len(set_to_study)
        cur_card = set_to_study.get_cards()[card_counter]
    
    ui.study_prompt(cur_card, card_counter, set_length)

    # Handle Key Presses
    term_showing = True
    while True:
        choice = getch.getch()
        if choice == ' ':
            if term_showing:
                ui.study_prompt(cur_card, card_counter, set_length, show_definition=True)
                term_showing = False
            else:
                ui.study_prompt(cur_card, card_counter, set_length)
                term_showing = True
        elif choice == 'q':
            set_view()
        elif choice == 's':
            if cur_card.get_is_starred():
                cur_card.set_is_starred(False)
                study_set(set_list, set_to_study, card_counter=card_counter, previous_cards=previous_cards, starred=starred)
            else:
                cur_card.set_is_starred(True)
                study_set(set_list, set_to_study, card_counter=card_counter, previous_cards=previous_cards, starred=starred)
        elif choice == 'h' and card_counter > 0:
            study_set(set_list, set_to_study, card_counter=card_counter - 1, previous_cards=previous_cards, prev_card=True, starred=starred)
        elif choice == 'l' and card_counter != set_length-1:
            if not prev_card:
                previous_cards.append(cur_card)
            study_set(set_list, set_to_study, card_counter=card_counter + 1, previous_cards=previous_cards, starred=starred)
        elif choice == 'r':
            set_to_study.reverse()
            study_set(set_list, set_to_study, card_counter=card_counter, previous_cards=previous_cards, prev_card=prev_card, starred=starred)
        elif card_counter == set_length-1:
            finished_studying_message = {
                'type': 'list',
                'name': 'post_studying_choice',
                'message': consts.FINISHED_STUDYING,
                'choices': [consts.STUDY_AGAIN, consts.STUDY_RESHUFFLE, consts.STUDY_STARRED, consts.EDIT_SET, consts.DELETE_SET, consts.GO_BACK]
            }

            try:
                finished_studying_choice = prompt(finished_studying_message)['post_studying_choice']
            except KeyError:
                save_set(set_list)
                raise SystemExit

            if finished_studying_choice == consts.STUDY_AGAIN:
                study_set(set_list, set_to_study, card_counter=0)
            elif finished_studying_choice == consts.STUDY_RESHUFFLE:
                set_to_study.shuffle()
                study_set(set_list, set_to_study, card_counter=0)
            elif finished_studying_choice == consts.STUDY_STARRED:
                study_set(set_list, set_to_study, card_counter=0, starred=True)
            elif finished_studying_choice == consts.EDIT_SET:
                edit_set(set_to_study)
                save_set(set_list)
                study_set(set_list, set_to_study, card_counter=0, starred=True)
            elif finished_studying_choice == consts.GO_BACK:
                save_set(set_list)
                set_view()


def set_view():
    try:
        set_choices = get_set_titles()

        set_list = retrieve_sets()

        set_choices.append(consts.ADD_SET)
        set_choices.append(consts.EXIT)
    except json.decoder.JSONDecodeError:
        set_list = []

        set_choices = [consts.ADD_SET, consts.EXIT]

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
            set_list[index_of_set] = edit_set(set_list[index_of_set], index_of_set)
        elif selected_set_choice == consts.STUDY_SET:
            set_list = retrieve_sets()
            set_list[index_of_set].shuffle()
            study_set(set_list, set_list[index_of_set])
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

    if os.path.isdir(consts.PATH_TO_SETS + '/sets.json'):
        print(consts.RED_BOLD, 'It seems like you have already initialized a storage file!')
    else:
        os.system('mkdir -p ' + consts.PATH_TO_SETS)
        os.system('touch ' + consts.PATH_TO_SETS + '/sets.json')

def dir_path(path):
    if path[:1] == '~/':
        path = os.path.relpath()
        path = str(Path.home()) + path

    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
    
def handle_arguments():
    args = argparse.ArgumentParser(description='A simple cli notecard application for studying...')
    args.add_argument('--init', help='initialize new file for storing sets.', action='store_true')
    args.add_argument('--delete', '-d', help='delete a set. Lists all the possible sets you can delete and allows for '
                                             'selection.', action='store_true')
    args.add_argument('--add', '-a', help='create a set', action='store_true')
    args.add_argument('--quick', '-q', help='skip intro animation...quickly start studying', action='store_true')
    args.add_argument('--convert', '-c', help='convert a quizlet set', type=argparse.FileType('r'))

    parser = args.parse_args()

    if parser.init:
        initialize()
    elif parser.quick:
        set_view()
    elif parser.convert:
        convert_quizlet(parser.convert)
    else:
        display_intro_animation()
        set_view()


def main():
    handle_arguments()


if __name__ == '__main__':
    main()
