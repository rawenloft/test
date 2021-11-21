'use strict'

document.addEventListener('DOMContentLoaded', function(){
    const notMe = document.querySelectorAll('.author');
    notMe.forEach(e => {
        e.addEventListener('click', event => {
            event.preventDefault();
            console.log(event);
        })
        let link = document.createElement("a");
        link.innerHTML = e.innerHTML.slice(3);
        link.setAttribute('href',`/${link.innerHTML}`);
        e.parentNode.replaceChild(link, e);
        console.log(e,link);
    })
})