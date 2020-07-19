"""constants for remembrall"""
import os
from pathlib import Path

# Path to sets or where sets will be stored
PATH_TO_SETS = str(Path.home()) + '/.config/remembrall'

# Get width and height of terminal
WIDTH, HEIGHT = os.get_terminal_size()

# Color Escape Code Constants
CYAN_BOLD =  '\u001b[1;36m'
CYAN =       '\u001b[0;36m'
RED_BOLD =   '\u001b[1;31m'
GREEN_BOLD = '\u001b[1;32m'
RESET =      '\u001b[0m'
INVISIBLE =  '\u001b[8m'
BOLD =       '\u001b[1m'
YELLOW =     '\u001b[0;33m'

# Prompts
EXIT =              'Exit'
ADD_SET =           'Add a Set'
BACK =              'Go Back'
INITIAL_PROMPT =    'Please select a set or make a new one.'
GENERIC_PROMPT =    'How would you like to proceed?'
EDIT_SET =          'Edit this Set'
STUDY_SET =         'Study this Shuffled Set'
STUDY_RANDOM =      'Study this Randomized Set'
GO_BACK =           'Go Back'
STUDY_AGAIN =       'Study the Set Again'
STUDY_RESHUFFLE =   'Study the Set Reshuffled'
STUDY_STARRED =     'Study the Starred Cards'
FINISHED_STUDYING = 'How would you like to continue studying?'

# card dimensions
CARD_WIDTH = WIDTH//7
CARD_HEIGHT = HEIGHT//7

# Instructions/Messages
STUDYING_INSTRUCTIONS = RESET + BOLD + 'Spacebar: shows the definition/term'.center(WIDTH) + '\n' + \
                        'h and l: to go back and forth - left and right respectively'.center(WIDTH) + '\n' + \
                        's: to star a missed card for future studying'.center(WIDTH) + '\n' + \
                        'q: to stop studying and go back'.center(WIDTH) + RESET
