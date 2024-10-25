# WikiLookup
Quickly lookup any word you want from Wikipedia directly from inside your decks!

*Link to add-on on ankiweb*: [WikiLookup](https://ankiweb.net/shared/info/1516720487)

## Usage
Simply double-click a word (or select a phrase) and press "W", and if Wikipedia has an article for it, it'll simply pop up a tooltip with an explanation and a picture. Convenient!

## Features
* Choose whichever keyboard shortcut that suits you
* Dark theme if you don't want your eyes to be scorched
* Choose the wiki in which your selected words will be looked up
* WikiLookup works with all 150+ languages available on Wikipedia
* Choose whether WikiLookup will always trigger or only when the card is flipped

# ⚠️ Important Note:
This repository has the source code for V2.0 of WikiLookup, which is drastically different from the version currently released on ankiweb, but has the same core idea. The idea behind V2.0 is to make the current language selection from the settings menu redundant, and instead automatically detect the language from the word/phrase selected and look it up in Wikipedia. The current implementation is a limitation from Wikipedia themselves, since they force you to select which language wiki to search in and don't have a global search engine. I've tried many solutions to get this to work. The one I landed on was to scrape a search engine's search results for the current phrase with Wikipedia as the top result (for eg. Google or DuckDuckGo), extract the link to the article, and proceed to fetch the data from the article to show the tooltip. This worked great on my computer. What I realised later is that search engines could easily detect you and ban you if you scrape their pages. *__This is the reason why V2.0 has not been released yet__*!. However, with the recent rise of A.I. language models, I have been planning to use a mini A.I. model whose only purpose is to detect the language so that the word can be looked up in Wikipedia.
*IF you have a suggestion to a better solution, please do not hesitate to contact me by starting an Issue thread, or emailing me at: [abdulraheemssulaiman@outlook.com](mailto:abdulraheemssulaiman@outlook.com)*
