$(".go-to-dbthing").click(function() {
    $('html, body').animate({
        scrollTop: $("#dbthing").offset().top
    }, 1000);
});
