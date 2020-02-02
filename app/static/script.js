var scroller = document.querySelector("#container");
var template = document.querySelector('#image_template');
var loaded = document.querySelector("#loaded");
var sentinel = document.querySelector('#sentinel');
var counter = 0;

function isAnyPartOfElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    const windowHeight = (window.innerHeight || document.documentElement.clientHeight);
    const windowWidth = (window.innerWidth || document.documentElement.clientWidth);
    const vertInView = (rect.top <= windowHeight) && ((rect.top + rect.height) >= 0);
    const horInView = (rect.left <= windowWidth) && ((rect.left + rect.width) >= 0);
    return (vertInView && horInView);
}

function getImages() {
    var dimensions = 0
    var ele = document.getElementsByName('dimensions');      
    for(i = 0; i < ele.length; i++) { 
        if(ele[i].checked) 
        dimensions = ele[i].value; 
    } 
    
    var greyscale = ""
    if (document.getElementById('greyscaleButton').checked) {
        greyscale = "&greyscale"
    }
    
    fetch(`/api/pictures?start=${counter}&dimensions=${dimensions}${greyscale}`).then((response) => {
        response.json().then((data) => {
            if (!data.length) {
                return
            }
            for (var i = 0; i < data.length; i++) {
                let template_clone = template.content.cloneNode(true);
                template_clone.querySelector("#content").src = "static/" + data[i]['url'];
                scroller.appendChild(template_clone);
                counter += 1;
                loaded.innerText = `${counter} items found`;
            }
        })
    })
}

var timerId;

var debounceFunction = function (func, delay) {
    if (timerId) {
        return
    }
    func();
    timerId = setTimeout(function () {
        timerId = undefined;
    }, delay)
}

function loadItems() {
    if (isAnyPartOfElementInViewport(sentinel)){
        debounceFunction(getImages, 1000);
    }
}

function reloadItems() {
    while (scroller.firstChild) {
        scroller.removeChild(scroller.firstChild);
    }
    counter = 0;
    loaded.innerText = `${counter} items found`;
    loadItems();
}
loadItems();
var poll = setInterval(loadItems, 500);

