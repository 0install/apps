function hideTabs() {
    $('.nav-tabs a.nav-link').removeClass('active');
    $('.tab-body').hide();
}

function showTab(name) {
    $('.nav-tabs a.nav-link[href="#' + name + '"]').addClass('active');
    $('#' + name + '-tab').show();
}

function updateTabs() {
    hideTabs();

    if (window.location.hash) {
        showTab(window.location.hash.slice(1));
    } else {
        history.replaceState({}, '', '#featured');
        showTab('featured');
    }
}

$(window).bind('hashchange', updateTabs);
$(function() { updateTabs(); });