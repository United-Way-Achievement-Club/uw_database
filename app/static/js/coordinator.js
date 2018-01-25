$(document).ready(function() {
    var location = window.location.pathname.split("/")[2];
    if (location == 'members') {
        $("#memberModalLabel").modal('hide');
    }
});

function memberModalChange(e) {
    var id = $(e).attr("id");
    $.get( "members/" + id, function() {
      console.log( "successfully requested html for modal change" );
      })
      .done(function(data) {
        console.log( "successfully received html for modal change" );
        $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
        $(e).addClass("member-modal-nav-item-active");
        $("#member-modal-body-component").html(data);
      })
      .fail(function() {
        console.log( "error receiving html for modal change" );
      })
      .always(function() {
        console.log( "retrieving modal change html" );
      });
}