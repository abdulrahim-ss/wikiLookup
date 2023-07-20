"""
    Module to check which theme is set for Anki and pass it through to the javascript code of the add-on in
    the webviewer to allow switching the tooltips theme between light and dark themes.
"""
from aqt.gui_hooks import theme_did_change
from aqt.theme import theme_manager
from aqt import mw

def decide_theme() -> bool:
    """
        Call set_dark_mode() or set_light_mode() located in 'web/wikiLookup.js' from within webviewer and
        return which theme is set, which is used in 'wiki_lookup.py' when add-on is first initialized.
    """
    darkmode = theme_manager.get_night_mode()
    if darkmode:
        mw.web.eval("set_dark_mode()")
    elif not darkmode:
        mw.web.eval("set_light_mode()")
    return darkmode

def init_theme_changer() -> None:
    theme_did_change.append(decide_theme)
