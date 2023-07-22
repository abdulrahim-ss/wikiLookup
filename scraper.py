import re
from requests import get
from urllib.parse import unquote
from typing import Union

# from .Config.config import lookup_language

class Scraper:
    """
        A web scraper class that queries a search engine (I opted for duckduckgo because it was the cleanest
        to handle) and parses out the relevant Wikipedia article from the result.
        
        For each looked-up word, the article displayed in the tooltip uses Scraper.lang and Scraper.title
        as its data.
    """
    def __init__(self) -> None:
        self.re_article_url = re.compile(r"(?P<whole>https://(?P<lang>\w{2,})\.wikipedia\.org/wiki/(?P<title>.+?))(?=&)")
        # self.re_ddg = re.compile(r"href=\"*(.+?)(?=&)")

        self.google_querier = "https://google.com/search?q=site%3Awikipedia.org+"
        self.ddg_querier = "https://html.duckduckgo.com/html?q=site:wikipedia.org+"

        self.preferred_lang = "english" #lookup_language
        self.matches = None
        self.article = None
        self.lang = None
        self.title = None

    def fetch_data(self, url: str, query: str) -> Union[str, None]:
        """
            The first layer of the lookup process. Handles only fetching the raw data from the search engine
        """
        raw = get(url + query, timeout=10, headers={"User-Agent":"Mozilla/6.0"}).text
        if not raw:
            print ("No response")
            return
        parsed = unquote(raw)
        return parsed

    def search(self, query: str) -> None:
        """
            Calls fetch_data and returns a filtered and parsed list of results data as an iterator saved to
            the object memory in Scraper.matches. Also sets the first search result data so that we have a
            starting article, and the user wouldn't need to explicitly cycle to it.
        """
        data = self.fetch_data(self.ddg_querier, query)
        if not data:
            return
        self.matches = self.re_article_url.finditer(data)
        try:
            self.article = next(self.matches)
        except StopIteration:
            return
        self.lang = unquote(self.article.group('lang'))
        self.title = unquote(self.article.group("title"))

    def next_article(self) -> None:
        """
            Called to cycle to the next article. Can only be called after search has been called once.
            Due to how DDG displays its search results, each article link is repeated at least once, so this
            method cycles through these articles in the iterator Scraper.matches until it finds the next new
            article and sets Scraper.lang and Scraper.title to the new articles data.
        """
        if not self.matches: return
        try:
            while True:
                current_article = next(self.matches)
                current_lang = unquote(current_article.group('lang'))
                current_title = unquote(current_article.group('title'))
                if current_lang != self.lang or current_title != self.title:
                    self.lang = current_lang
                    self.title = current_title
                    self.article = current_article
                    return
        except StopIteration:
            pass


if __name__ == "__main__":
    scraper = Scraper()
    query = "Saltvatten"

    data = scraper.fetch_data(scraper.ddg_querier, query)
    with open("etc/search.html", "w", encoding="utf-8") as f:
        f.write(data)
        f.close()

    # while True:
    #     inp = input()
    #     if inp == "next":
    #         scraper.next_article()
    #     else:
    #         scraper.search(inp)
    #     print(scraper.lang, "\t\t", scraper.title, "\n\n")
