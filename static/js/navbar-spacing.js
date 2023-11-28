// navbar-spacing.js

// Adjust content margin based on navbar height
function adjustContentMargin() {
    var navbarHeight = $(".navbar").outerHeight();
    $(".content-wrapper").css("margin-top", navbarHeight + "px");
}

// Call the function on document ready and window resize
$(document).ready(function () {
    adjustContentMargin();
});

$(window).resize(function () {
    adjustContentMargin();
});
