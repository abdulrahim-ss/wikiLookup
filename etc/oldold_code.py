# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect

from aqt import gui_hooks

def prepare(html, card, context):
    lookup_on = "///////////////////WikiLookup is enabled///////////////////"

    if context != "reviewAnswer" or lookup_on in html:
        return html

    style = """
    <style>
    .wiki-thumb {
    width: calc(100% - 1.2em);
    /*max-width: 20vw;*/
    margin: 0.56em;
    }

    .tippy-box[data-theme~=wiki] {
    background-color: white;
    box-shadow: 0px 5px 15px 0px rgba(0, 0, 0, 0.3);
    padding: 0;
    font-size: 16px;
    color: black;
    cursor: pointer;
    min-width: 300px;
    min-height: 200px;
    }

    [data-theme~=wiki] .tippy-arrow {
    color: white;
    }

    [data-theme~=wiki] .tippy-content {
    padding: 0;
    }

    .tippy-wiki-blurb {
    padding: 0 0.4em 0.4em 0.8em;
    text-align: left;
    }

    .tippy-box[data-animation=scale-extreme][data-placement^=top] {
    transform-origin: bottom
    }

    .tippy-box[data-animation=scale-extreme][data-placement^=bottom] {
    transform-origin: top
    }

    .tippy-box[data-animation=scale-extreme][data-placement^=left] {
    transform-origin: right
    }

    .tippy-box[data-animation=scale-extreme][data-placement^=right] {
    transform-origin: left
    }

    .tippy-box[data-animation=scale-extreme][data-state=hidden] {
    transform: scale(0);
    opacity: .25
    }

    #temp {
    top: 0;
    left: 0;
    position: absolute;
    pointer-events: none;
    }
    </style>
    """
    popper = "<script src=\"https://unpkg.com/@popperjs/core@2\"></script>"
    tippy = "<script src=\"https://unpkg.com/tippy.js@6\"></script>"
    wikiLookup ="""
    <script>
        ///////////////////WikiLookup is enabled///////////////////
        if(document.getElementById('temp') == null){
        const temp = document.createElement("div")
        temp.setAttribute("id", "temp")
        document.body.appendChild(temp)
        }


        ////////////////////////main///////////////////////////////
        window.addEventListener("keydown", async function (event) {
        if (event.key != 'w') return

        let sel_element = window.getSelection()
        let lookUpTxt = sel_element.toString().trim()

        if (lookUpTxt == "") return

        let pos = sel_element.getRangeAt(0).getBoundingClientRect()

        temp.style.left = `calc(${pos.left}px + ${pos.width / 2}px)`
        let placement = "bottom"
        if (pos.top > window.innerHeight / 2) {
            temp.style.top = `${pos.top}px`
            placement = "top"
        }
        else {
            temp.style.top = `calc(${pos.top}px + ${pos.height}px)`
        }
        await createWikiToolTip("en", lookUpTxt, placement)
        })
        //////////////////////main end/////////////////////////////


        async function createWikiToolTip(lang, search, placement) {
        let wiki = document.createElement("div")
        let thumbnail = new Image()
        let blurb = document.createElement("div")

        thumbnail.classList.add("wiki-thumb")
        wiki.classList.add("tippy-wiki")
        blurb.classList.add("tippy-wiki-blurb")

        let previewData = await createWikiPreview(lang, search)

        thumbnail.src = previewData.thumbSrc
        blurb.innerHTML = previewData.blurbTxt
        wiki.appendChild(thumbnail)
        wiki.appendChild(blurb)

        var [instance] = tippy("#temp", {
            content: wiki,
            sticky: true,
            theme: "wiki",
            appendTo: document.body,
            delay: [100, 100],
            touch: ["hold", 300],
            animation: "scale-extreme",
            placement: placement
        })
        instance.show()
        }

        async function createWikiPreview(lang, search) {
        let thumbParams = {
            action: "query",
            format: "json",
            prop: "pageimages",
            pithumbsize: 400,
        }

        let blurbParams = {
            action: "query",
            format: "json",
            prop: "extracts",
            exsentences: 2,
            exintro: 1,
        }
        let title = await getTitle(lang, search)
        let thumbSrc = await getData(lang, title, thumbParams)
        let blurbTxt = await getData(lang, title, blurbParams)
        thumbSrc = thumbSrc.thumbnail.source
        blurbTxt = blurbTxt.extract
        let previewData = {
            "title": title,
            "thumbSrc": thumbSrc,
            "blurbTxt": blurbTxt
        }
        return previewData
        }

        async function getData(lang, title, params) {
        params.titles = title
        let url = wikiUrl(lang, params)
        let response = await wikiFetch(url)
        let pages = response.query.pages
        return pages[Object.keys(pages)[0]]
        }

        async function getTitle(lang, search) {
        var titleParams = {
            action: "query",
            list: "search",
            format: "json",
            srlimit: 1,
            srsearch: search,
            srwhat: "text"
        };
        let url = wikiUrl(lang, titleParams)
        let response = await wikiFetch(url)
        let title = response.query.search[0].title
        return title
        }

        var wikiUrl = (lang, params) => {
        let url = `https://${lang}.wikipedia.org/w/api.php`;
        url = url + "?origin=*";
        Object.keys(params).forEach(function (key) {
            url += "&" + key + "=" + params[key]
        })
        return url
        }

        async function wikiFetch(url) {
        return new Promise((resolve, reject) => {
            fetch(url)
            .then(function (response) { return response.json(); })
            .then(function (response) {
                resolve(response)
            })
            .catch(function (error) { console.log(error); });
        })
        }
    </script>
"""
    return html + style + popper + tippy + wikiLookup

# gui_hooks.reviewer_did_answer_card.remove(prepare)
gui_hooks.card_will_show.append(prepare)
