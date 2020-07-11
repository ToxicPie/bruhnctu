document.addEventListener('DOMContentLoaded', (e) => {
    // add click for spoilers
    for(const elem of document.getElementsByClassName('spoiler')) {
        elem.setAttribute('tabindex', '-1');
        elem.setAttribute('title', 'You\'ve known too much.');
    }
    // click to hide alert
    for(const elem of document.getElementsByClassName('close-button')) {
        elem.addEventListener('click', (e) => {
            if(e.target === elem)
                elem.parentElement.classList.add('hidden');
        });
    }
    if(document.getElementsByClassName('toc').length !== 0 &&
        document.getElementById('toc-container') !== null) {
        let toc = document.getElementsByClassName('toc')[0];
        document.getElementById('toc-container').appendChild(toc);
    }
});
