
class Set(object):
    def __init__(self, _title, _cards):
        self._title = self.set_title(_title)
        self._cards = _cards

    def add_cards(self, card_list):
        # if set is empty
        pass
    
    def set_title(self, _title):
        self._title = _title

    def get_title(self):
        return self._title

class Card(object):
    def __init__(self, _term, _definition):
        self._term = self.set_term(_term)
        self._definition = self.set_definition(_definition)

    def set_definition(self, _definition):
        self._definition = _definition

    def get_definition(self):
        return self._definition

    def set_term(self, _term):
        self._term = _term

    def get_term(self):
        return self._term