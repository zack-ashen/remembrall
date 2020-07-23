import random

import ui
import consts

class Set(object):
    def __init__(self, _title, _cards, _starred_cards=[]):
        self.set_title(_title)
        self._cards = _cards
        self._starred_cards = _starred_cards

    def add_cards(self, card_list):
        # if set already has cards
        pass

    def add_starred_card(self, card):
        self._starred_cards.append(card)
    
    def set_title(self, _title):
        self._title = _title

    def get_title(self):
        return self._title
    
    def to_list(self):
        card_list = []
        for card in self._cards:
            card_item = [card.get_term(), card.get_definition()]
            card_list.append(card_item)
        return card_list

    def get_cards(self):
        return self._cards

    def get_random_card(self):
        random_card_index = random.choice(range(len(self._cards)))
        return self._cards[random_card_index]

    def shuffle(self):
        random.shuffle(self.get_cards())

    def get_starred_cards(self):
        for card in self.get_cards():
            if card.get_is_starred():
                self.add_starred_card(card)

        return self._starred_cards

    def __len__(self):
        return len(self.get_cards())


class Card(object):
    def __init__(self, _term, _definition, _is_starred=False):
        self.set_term(_term)
        self.set_definition(_definition)
        self.set_is_starred(_is_starred)

    def set_is_starred(self, is_starred):
        self._is_starred = is_starred

    def get_is_starred(self):
        return self._is_starred

    def set_definition(self, definition):
        self._definition = definition

    def get_definition(self):
        return self._definition

    def set_term(self, term):
        self._term = term

    def get_term(self):
        return self._term

    def display_term(self):
        if self.get_is_starred():
            ui.print_colored_card(consts.YELLOW, consts.CARD_WIDTH, consts.CARD_HEIGHT, self.get_term(), is_term=True)
        else:
            ui.print_colored_card(consts.CYAN, consts.CARD_WIDTH, consts.CARD_HEIGHT, self.get_term(), is_term=True)

    def display_definition(self):
        if self.get_is_starred():
            ui.print_colored_card(consts.YELLOW, consts.CARD_WIDTH, consts.CARD_HEIGHT, self.get_definition())
        else:
            ui.print_colored_card(consts.CYAN, consts.CARD_WIDTH, consts.CARD_HEIGHT, self.get_definition())

