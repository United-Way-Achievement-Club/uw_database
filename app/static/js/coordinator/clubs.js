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
}

function saveClubModal() {
    closeClubModal();
}