$(document).ready(function() {
    var location = window.location.pathname.split("/")[2];
    $(".active").removeClass("active");
    $("#" + location).addClass("active");

    if (location == 'members') {
        $("#memberModalLabel").modal('hide');
    }
});