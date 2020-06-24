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

from PyInquirer import prompt
from pyfiglet import Figlet
import argparse

from set import Set, Card

# Get width and height of terminal
width, height = os.get_terminal_size()

# Find card width and height based on terminal width
card_width = round(width / 1.5)
card_height = round(card_width / 4)

# Color Escape Code Constants
CYAN_BOLD = '\u001b[1;36m'
CYAN = '\u001b[0;36m'
RED_BOLD = '\u001b[1;31m'
GREEN_BOLD = '\u001b[1;32m'
RESET = '\u001b[0m'

# PyInquirer Options
EXIT = 'Exit'
ADD_SET = 'Add a Set'
BACK = 'Go Back'

# set paths for sets file
home_dir_path = str(Path.home())
path_to_config = home_dir_path + '/.config/remembrall'


def print_colored_card(border_color, background_color, card_width, card_height):
    """
    :param border_color: Is a string ANSI escape code for the border color, should only contain a foreground color not
    a background.
    :param background_color:  Is a string ANSI escape code for the background color, should only contain a background
    color.
    """
    i = 0

    offset_width = round((width - card_width) / 2) - 2
    print(border_color, end='')
    print(' ' * offset_width + '┌' + '─' * card_width + '┐')
    while i < card_height:
        print(' ' * offset_width, end='')
        print(border_color, end='')
        print('│', end='')
        print(background_color, end='')
        print(' ' * card_width, end='')
        print(RESET, end='')
        print(border_color, end='')
        print('│')
        i += 1
    print(' ' * offset_width + '└' + '─' * card_width + '┘')


def saveSet(set_list):
    set_dict = {}
    for set in set_list:
        set_dict[set.get_title()] = set.get_cards()


def retrieve_sets():
    setsFile = open(path_to_config + '/sets.json')


    return set_list

def get_set_titles():
    set_list = retrieve_sets()

    set_titles = []
    for set in set_list:
        set_titles.append(set.get_title())
    return set_titles

def set_title_prompt():
    set_title_prompt = {
        'type': 'input',
        'name': 'set_name',
        'message': 'What should the name of the set be?',
        'type': 'input'
    }
    set_title_input = prompt(set_title_prompt)
    return set_title_input['set_title']

def make_cards():
    continue_adding_cards = True
    card_list = []
    while continue_adding_cards:
        add_card_prompt = {
            'type': 'input',
            'name': 'card_term',
            'message': 'What should be the card term? (Enter \'-\' to finish)',
        },
        {
            'type': 'input',
            'name': 'card_definition',
            'message': 'What should the card definition be? (Enter \'-\' to finish)'
        }
        card_details = prompt(add_card_prompt)

        card_term = card_details['card_term']
        card_definition = card_details['card_definition']
        if card_term == '-' or card_definition == '-':
            continue_adding_cards = False
        else:
            new_card = Card(card_term, card_definition)
            card_list.append(new_card)
        return card_list

def make_a_set():
    # clear screen
    os.system('clear')

    # print a card to make stuff look cool
    print_colored_card(CYAN_BOLD, CYAN, card_width, card_height)

    # get a title for the set
    set_title = set_title_prompt()

    # add cards to set
    card_list = make_cards()

    return Set(set_title, card_list)


def set_view():
    try:
        set_choices = get_set_titles()
        set_choices.append(ADD_SET, EXIT)
    except:
        set_choices = [ADD_SET, EXIT]
    set_options_prompt = {
        'type': 'list',
        'name': 'option_selection',
        'message': 'Please select an set or make a new one.',
        'choices': set_choices
    }
    set_options = prompt(set_options_prompt)


def display_intro_animation():
    title = 'remembrall...'
    fig = Figlet(font='stop', justify='center', width=width)

    print(CYAN_BOLD)

    # animate welcome text
    title_accumulator = ''
    for character in title:
        sleep(0.1)
        os.system('clear')
        title_accumulator += character
        # center text vertically
        print('\n' * round(height / 5))
        print(fig.renderText(title_accumulator))
    set_view()


def initialize():
    # initialize folder in .config folder to store all of the sets in json
    if os.path.isdir(path_to_config):
        print(RED_BOLD, 'It seems like you have already initialized a config!')
    else:
        os.system('mkdir -p ' + path_to_config)
        os.system('touch ' + path_to_config + '/sets.json')


def handle_arguments():
    args = argparse.ArgumentParser(description='A simple cli notecard application for studying...')
    args.add_argument('--init', help='initialize new file for storing sets.', action='store_true')
    args.add_argument('--delete', '-d', help='delete a set. Lists all the possible sets you can delete and allows for select'
                                       'ion.', action='store_true')
    args.add_argument('--add', '-a', help='create a set', action='store_true')
    args.add_argument('--quick', '-q', help='skip intro animation...quickly start studying', action='store_true')
    args.add_argument('--import', '-i', help='import a quizlet set')

    parser = args.parse_args()
    if parser.init:
        initialize()
    elif parser.quick:
        set_view()
    else:
        hi = Set('hi', ['huh'])
        display_intro_animation()


def main():
    handle_arguments()
    #display_intro_animation()


if __name__ == '__main__':
    main()
