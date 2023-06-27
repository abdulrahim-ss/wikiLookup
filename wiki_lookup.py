from os.path import dirname, realpath
from pathlib import Path

from aqt import mw
from aqt.gui_hooks import webview_will_set_content
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

from .Config.config import lookup_trigger, lookup_language, backside
from .theme_manager import decide_theme

class wikiLookup:
    def __init__(self):
        print("EnableJSAddon initialized")
        mw.addonManager.setWebExports(__name__, r"(web|Config)/.*\.(js|css|svg|json)")
        # self.injected_cards = set()
        webview_will_set_content.append(self.on_webview_will_set_content)
        # gui_hooks.reviewer_did_show_answer.append(self.on_reviewer_did_show_answer)

    def on_webview_will_set_content(self, web_content: WebContent, context):
        if not isinstance(context, Reviewer):
            # not reviewer, do not modify content
            return

        # reviewer, perform changes to content

        context: Reviewer

        addon_package = mw.addonManager.addonFromModule(__name__)

        popper = "<script src=\"https://unpkg.com/@popperjs/core@2\"></script>"
        tippy = "<script src=\"https://unpkg.com/tippy.js@6\"></script>"
        theme = "globalThis.theme = \"wikilight\";\n"
        if decide_theme(): theme = "globalThis.theme = \"wikidark\";\n"

        web_content.head += popper + tippy

        web_content.css.append(
            f"/_addons/{addon_package}/web/wikiLookup.css")

        web_content.head += ("<script>" + f"globalThis.lookup_trigger = \"{lookup_trigger.value}\";\n" + \
                             f"globalThis.lookup_language = \"{lookup_language.value}\";\n" + \
                             f"globalThis.backside = {str(backside.value).lower()};\n" + \
                             theme + \
                             "</script>")

        web_content.js.append(
            f"/_addons/{addon_package}/web/addon_trigger.js")
        web_content.js.append(
            f"/_addons/{addon_package}/web/wikiLookup.js")

    def get_source(self, source_name):
        filepath = Path(dirname(realpath(__file__)), source_name)

        with open(filepath, mode="r", encoding="utf-8") as file:
            return file.read()
