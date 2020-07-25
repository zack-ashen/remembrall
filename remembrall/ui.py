"""module with functions related to ui and design"""

import os

import consts


def print_dividing_line():
    for char in range(consts.WIDTH):
        print('─', end='')
    print('')


def print_colored_card(border_color, card_width, card_height, text, is_term=False):
    print(border_color, end='')
    print(('┌' + '─' * card_width + '┐').center(consts.WIDTH))

    i = 0
    while i < card_height:
        print(border_color, end='')
        if i == card_height // 2:
            if is_term:
                print(consts.BOLD, end='')
            print(('│' + text.center(card_width) + '│').center(consts.WIDTH))
        else:
            print(('│' + ' ' * card_width + '│').center(consts.WIDTH))
        i += 1
    print(('└' + '─' * card_width + '┘').center(consts.WIDTH))


def study_prompt(card, card_counter, set_length, show_definition=False):
    os.system('clear')

    print('\n' * (consts.HEIGHT // 2 - (5 + consts.CARD_HEIGHT)))
    print(('Card ' + str(card_counter + 1) + '/' + str(set_length)).center(consts.WIDTH))

    if show_definition:
        card.display_definition()
    else:
        card.display_term()

    print(consts.STUDYING_INSTRUCTIONS)
