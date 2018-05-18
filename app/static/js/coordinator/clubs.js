$(document).ready(function() {
// TODO: figure this out !!
//    $('#tokenfield').tokenfield({
//      autocomplete: {
//        source: ['red','blue','green','yellow','violet','brown','purple','black','white'],
//        delay: 100
//      },
//      showAutocompleteOnFocus: true
//    })
})

function showClubDetails(club) {
    $("#club-details").show();
}

function hideClubDetails() {
    $("#club-details").hide();
}

function openClubModal() {
// TODO: figure this out !!
//    $("#tokenfield").tokenfield();
//    $('#tokenfield').tokenfield({
//      autocomplete: {
//        source: ['red','blue','green','yellow','violet','brown','purple','black','white'],
//        delay: 100
//      },
//      showAutocompleteOnFocus: true
//    });
}

function closeClubModal() {
    $("#clubModal").modal('hide');
    $(".club-modal-body input").val("");
    $("#club-coordinators .club-coord").not(":first").remove();
}

function saveClubModal() {
    closeClubModal();
}

function addClubCoord() {
    var clubCoordInputs = $(".club-coord-input-extra").length;
    if (clubCoordInputs >= 4) {
        window.alert("Sorry, you can't add more than 4 coordinators per club.");
    } else {
        var clubCoord = $("#hidden-coord-input").html();
        $("#club-coordinators").append(clubCoord);
    }
}

function removeCoordinator(e) {
    var parent = $(e).parent();
    var grandparent = $(parent).parent()
    $(grandparent).remove();
}