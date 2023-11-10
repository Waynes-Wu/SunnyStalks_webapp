document.addEventListener("DOMContentLoaded", function() {
    // Get all icons
    var icons = document.querySelectorAll('.fab-list>li>i');

    icons.forEach((icon) => {
        icon.addEventListener('click', function() {
            var link = icon.dataset.action;
            if (link != null)
                window.location.href = link;
        });
    });
});