// Uses hideTabs()/showTab() from https://0install.net/js/site.js

function updateTabs() {
    hideTabs();

    if (window.location.hash) {
        showTab(window.location.hash.slice(1));
    } else {
        history.replaceState({}, '', '#catalog');
        showTab('catalog');
    }
}

addEventListener('hashchange', updateTabs);
updateTabs();
