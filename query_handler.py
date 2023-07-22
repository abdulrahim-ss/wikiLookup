import json
from typing import Tuple, Union, Any
import json

from aqt.gui_hooks import webview_did_receive_js_message
from aqt.reviewer import Reviewer
from aqt import mw

from .scraper import Scraper

class Query_Handler:
    """
        A class that handles the communication of data between the websearch querying part of code and
        the webviewer using pycmd() to communicate webviewer -> Python, 
        and mw.web.eval() to communicate Python -> webviewer
    """
    def __init__(self):
        self.scraper = Scraper()
        webview_did_receive_js_message.append(self.handle_search_query)

    def handle_search_query(self, handled: Tuple[bool, Any], message: str, context: Any) -> Tuple[bool, Any]:
        """
            Get search query from webviewer through pycmd (which is used by 'wikiLookup.js'),
            and send the search result (saved in the object memory of scraper) to the webviewer as a JSON object
        """
        if not isinstance(context, Reviewer):
            return handled
        if message[0] != "{": return handled

        action = self.action(message)
        if not action: return handled
        if not self.scraper.article: return handled
        result = {"lang": self.scraper.lang, "title": self.scraper.title}

        response =  json.dumps(result)
        # For some reason I can't send the response as a value to pycmd()'s callback on the webviewer side
        # so I used a workaround method, which is to evaluate that a variable called "search_result" in the
        # webviewer's javascript code is to be equal to our response generated here.
        mw.web.eval(f"search_result = {response}")
        #mw.web.eval(f"console.log(`{message} received by the python side of the wikiLookup add-on`)")
        #mw.web.eval(f"console.log(`python responded with {message}`)")
        return (True, None)
    
    def action(self, message: str) -> Union[str, None]:
        """
            Cheack what action is requested by the webviewer and run corresponding method in Scraper class.
        """
        msg = json.loads(message)
        if msg["action"] == "search":
            self.scraper.search(msg["message"])
            return msg["message"]
        elif msg["action"] == "next":
            self.scraper.next_article()
            return "next"
        else:
            return None
