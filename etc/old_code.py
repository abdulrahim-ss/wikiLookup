# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
#from aqt.qt import *
# import the "show info" tool from utils.py

from aqt import gui_hooks

from os.path import dirname, realpath
from pathlib import Path

import re

mw.addonManager.setWebExports(__name__, r"web/.*\.(js|css|svg)")

def get_source(source_name):
        filepath = Path(dirname(realpath(__file__)), source_name)

        with open(filepath, mode="r", encoding="utf-8") as file:
            return file.read()

def prepare(html, card, context):
    lookup_on = "<!--/////////////////WikiLookup is enabled//////////////////-->"

    match = re.search(lookup_on, html)

    if context != "reviewAnswer" or match:
        return html

    popper = "<script src=\"https://unpkg.com/@popperjs/core@2\"></script>"
    tippy = "<script src=\"https://unpkg.com/tippy.js@6\"></script>"

    wikiLookup = "<script>" + get_source('web/wikiLookup.js') + "</script>"
    style = "<style>" + get_source("web/wikiLookup.css") + "</style>"

    return html + style + popper + tippy + wikiLookup

# gui_hooks.reviewer_did_answer_card.remove(prepare)
try:
    gui_hooks.card_will_show.remove(prepare)
except: 
    pass
gui_hooks.card_will_show.append(prepare)
