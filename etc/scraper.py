import re
from requests import get
from urllib import parse

re_google = re.compile(r"(?P<whole>https://(?P<lang>\w{2,})\.wikipedia\.org/wiki/(?P<title>.+?))(?=&)")
re_ddg = re.compile(r"href=\"*(.+?)(?=&)")
google_query = "https://google.com/search?q=site%3Awikipedia.org+"
ddg_query = "https://html.duckduckgo.com/html?q=site:wikipedia.org+"

preferred_lang = "sv"

def fetch_data(url, query):
    raw = get(url + query, timeout=10, headers={"User-Agent":"Mozilla/6.0"}).text
    if not raw:
        print ("No response")
        exit()
    parsed = parse.unquote(raw)
    return parsed

def matching_article(url, query):
    # print(query, parse.quote(query))
    data = fetch_data(url, query)
    with open("search.html", "w", encoding="utf-8") as f:
        f.write(data)
    matches = re_google.finditer(data)
    if not matches:
        print("Something went wrong")
        return

    first_article = next(matches)
    current_lang = first_article.group('lang')
    title = first_article.group("title")

    # if current_lang == preferred_lang and title == query:
    #     return (current_lang, title)
    #     if article.group('lang') == preferred_lang and query in article.group("title"):
    #         current_lang = article.group("lang")
    #         title = article.group("title")
    #         return (current_lang, title)

    # print("no matching articles were found")
    # return (current_lang, title)

if __name__ == "__main__":
    query = preferred_lang + "lego"
    # matching_article(ddg_query, query)
    # print(response)
    resp = fetch_data(ddg_query, query)
    for i in re.finditer(re_google, resp):
        print(parse.unquote(i.group(1)), "\n")
