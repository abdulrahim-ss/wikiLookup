if(document.getElementById('temp') === null){
const temp = document.createElement("div")
temp.setAttribute("id", "temp")
document.body.appendChild(temp)
}

card_is_flipped = false;
const question_is_shown = () => {
    card_is_flipped = false;
}
const answer_is_shown = () => {
    card_is_flipped = true;
}

set_dark_mode = () => {
    globalThis.theme = "wikidark"
}
set_light_mode = () => {
    globalThis.theme = "wikilight"
}

////////////////////////main///////////////////////////////
window.addEventListener("keydown", async function (event) {
//if (event.key != 'W') return
if (!eval(globalThis.lookup_trigger_condition)) return
if (globalThis.backside && !card_is_flipped) return
let sel_element = window.getSelection()
let lookUpTxt = sel_element.toString().trim()

if (lookUpTxt === "") return

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
await createWikiToolTip(lookUpTxt, placement)
})
//////////////////////main end/////////////////////////////

const icon = () => {
    let v = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    v.setAttribute("height", "1em");
    v.setAttribute("viewBox", "0 0 320 512");
    let p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute("d", "M310.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-192 192c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L242.7 256 73.4 86.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l192 192z");
    v.appendChild(p);
    return v;
}

async function createWikiToolTip(search, placement) {
    let search_result = {}
    let wiki = document.createElement("div")
    let thumbnail = new Image()
    let blurb = document.createElement("div")
    let refresh = document.createElement("button")

    thumbnail.classList.add("wiki-thumb")
    wiki.classList.add("tippy-wiki")
    blurb.classList.add("tippy-wiki-blurb")
    refresh.classList.add("tippy-refresh-button")
    refresh.setAttribute("title", "Show next matching article")
    refresh.appendChild(icon())

    msg = {"action": "search", "message": search}
    pycmd(JSON.stringify(msg))
    let previewData = await createWikiPreview(search_result.lang, search_result.title)
    
    refresh.addEventListener('click', async () => {
        msg = {"action": "next", "message": ""}
        pycmd(JSON.stringify(msg))
        let previewData = await createWikiPreview(search_result.lang, search_result.title)
        thumbnail.src = previewData.thumbSrc
        blurb.innerHTML = previewData.blurbTxt
    })

    thumbnail.src = previewData.thumbSrc
    blurb.innerHTML = previewData.blurbTxt
    wiki.appendChild(thumbnail)
    wiki.appendChild(blurb)
    wiki.appendChild(refresh)

    var [instance] = tippy("#temp", {
        allowHTML: true,
        content: wiki,
        sticky: true,
        theme: globalThis.theme,
        appendTo: document.body,
        //delay: [100, 100],
        touch: ["hold", 300],
        animation: "scale-extreme",
        placement: placement,
        interactive: true,
        cursor: 'default',
    })
    instance.show()
}

async function createWikiPreview(lang, title) {
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
    let response = await fetcher(url)
    let pages = response.query.pages
    return pages[Object.keys(pages)[0]]
}

/************* DEPRECATED ************/
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
///////////////////////////////////////

var wikiUrl = (lang, params) => {
    let url = `https://${lang}.wikipedia.org/w/api.php`;
    url = url + "?origin=*";
    Object.keys(params).forEach(function (key) {
        url += "&" + key + "=" + params[key]
    })
    return url
}

async function fetcher(url) {
    return new Promise((resolve, reject) => {
        fetch(url)
        .then(function (response) { return response.json(); })
        .then(function (response) {
            resolve(response)
        })
        .catch(function (error) { console.log(error); });
    })
}