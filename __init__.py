"""
    This is the module that Anki calls when it tries to initialize an add-on. All other python modules in the
    add-on should be initialized and called here for Anki to be able to run them.
"""

from .wiki_lookup import wikiLookup
from .Config.add_on import configDialogue
from .check_reviewer import reviewer_checker
from .theme_manager import init_theme_changer
from .query_handler import Query_Handler

wikiLookup()
Query_Handler()
configDialogue()
init_theme_changer()
reviewer_checker()
