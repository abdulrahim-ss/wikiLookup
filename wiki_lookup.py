from os.path import dirname, realpath
from pathlib import Path
from typing import Any

from aqt import mw
from aqt.gui_hooks import webview_will_set_content
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

from .Config.config import lookup_trigger, lookup_language, backside
from .theme_manager import decide_theme

class wikiLookup:
    """
        wikiLookup is the injector class, responsible for injecting, configuring, and initializing
        the add-on's code in Anki's webview. It injects the javascript and css code in webview (only when
        the context is Reviewer, i.e. the reviewer is active), which is reesponsible for generating the
        pop-up tooltips for the Lookup word.
    """
    def __init__(self):
        """
            __init__ method in all of wikiLookup's classes are responsible of binding the functionality of
            the class to Anki's hooks. This particular __init__ allows on_webview_will_set_content method to
            be called whenever a webview is initialized, i.e. whenever a user navigates to a new window/context.
        """
        # in order for our add-on to be able to access assets contained within the add-on package and use it
        # from within Anki, we need to use 'setWebExports'
        mw.addonManager.setWebExports(__name__, r"(web|Config)/.*\.(js|css|svg|json)")
        webview_will_set_content.append(self.on_webview_will_set_content)

    def on_webview_will_set_content(self, web_content: WebContent, context: Any) -> None:
        """
            Inject popper and tippy.js into Anki's webviewer, as well as wikiLookup's code which generates
            the pop-up tooltips for the words. This method also passes through Anki's set theme which allows
            the add-on to support light and dark themes.
        """
        if not isinstance(context, Reviewer):
            # not reviewer, do not modify content
            return

        addon_package = mw.addonManager.addonFromModule(__name__)

        popper = "<script src=\"https://unpkg.com/@popperjs/core@2\"></script>"
        tippy = "<script src=\"https://unpkg.com/tippy.js@6\"></script>"
        theme = "globalThis.theme = \"wikilight\";\n"
        if decide_theme(): theme = "globalThis.theme = \"wikidark\";\n"

        web_content.head += popper + tippy

        web_content.css.append(
            f"/_addons/{addon_package}/web/wikiLookup.css")

        web_content.head += ("<script>\n" + f"globalThis.lookup_trigger = \"{lookup_trigger.value}\";\n" + \
                            #  f"globalThis.lookup_language = \"{lookup_language.value}\";\n" + \
                             f"globalThis.backside = {str(backside.value).lower()};\n" + \
                             theme + \
                             "\n</script>")

        web_content.js.append(
            f"/_addons/{addon_package}/web/addon_trigger.js")
        web_content.js.append(
            f"/_addons/{addon_package}/web/wikiLookup.js")

    def get_source(self, source_name: str) -> str:
        """
        [UNUSED]
        This method is deprecated in wikiLookup, but is still included because it might be useful for other
        add-on developers. It can read files from within the add-on's package folder, but can be modified to
        access any file on the user's device. Unsecure and unrecommended.
        However, I have used the same technique in 'Config/add_on.py' to access the list of Wikipedias available.
        """
        filepath = Path(dirname(realpath(__file__)), source_name)

        with open(filepath, mode="r", encoding="utf-8") as file:
            return file.read()
