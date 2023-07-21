import re
from requests import get
from urllib.parse import unquote
from typing import Union, Dict

# from .Config.config import lookup_language

class Scraper:
    def __init__(self) -> None:
        self.re_article_url = re.compile(r"(?P<whole>https://(?P<lang>\w{2,})\.wikipedia\.org/wiki/(?P<title>.+?))(?=&)")
        # self.re_ddg = re.compile(r"href=\"*(.+?)(?=&)")

        self.google_querier = "https://google.com/search?q=site%3Awikipedia.org+"
        self.ddg_querier = "https://html.duckduckgo.com/html?q=site:wikipedia.org+"

        self.preferred_lang = "english" #lookup_language
        self.matches = None

    def fetch_data(self, url: str, query: str) -> Union[str, None]:
        raw = get(url + query, timeout=10, headers={"User-Agent":"Mozilla/6.0"}).text
        if not raw:
            print ("No response")
            return
        parsed = unquote(raw)
        return parsed

    def search(self, query: str) -> None:
        data = self.fetch_data(self.ddg_querier, query)
        if not data:
            return
        self.matches = self.re_article_url.finditer(data)
        if not self.matches:
            return

    def matching_article(self) -> Union[None, Dict[str, str]]:
        if not self.matches: return
        current_article = next(self.matches)
        current_lang = unquote(current_article.group('lang'))
        title = unquote(current_article.group("title"))
        return {"lang": current_lang, "title": title}

    # if current_lang == preferred_lang and title == query:
    #     return (current_lang, title)
    #     if article.group('lang') == preferred_lang and query in article.group("title"):
    #         current_lang = article.group("lang")
    #         title = article.group("title")
    #         return (current_lang, title)

    # print("no matching articles were found")
    # return (current_lang, title)

if __name__ == "__main__":
    scraper = Scraper()
    query = scraper.preferred_lang + "run-on sentences"
    resp = scraper.fetch_data(scraper.ddg_querier, query)
    if not resp: exit()
    for i in re.finditer(scraper.re_article_url, resp):
        print(unquote(i.group(1)), "\n")
