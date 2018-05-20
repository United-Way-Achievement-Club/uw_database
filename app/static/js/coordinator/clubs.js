function showClubDetails(club) {
    $("#" + club).show();
}

function hideClubDetails() {
    $(".club-details").hide();
}

function openClubModal() {

}

function closeClubModal() {
    $("#clubModal").modal('hide');
    $(".club-modal-body input").val("");
    $("#club-coordinators .club-coord").not(":first").remove();
}

function saveClubModal() {
    var clubVals = $("#club-form").serializeArray();
    var clubObj = {"coordinators": []};
    for (x in clubVals) {
        if (clubVals[x].name === "coordinator_name" ) {
            if (clubVals[x].value !== "") {
                clubObj.coordinators.push(clubVals[x].value);
            }
        } else {
            clubObj[clubVals[x].name] = clubVals[x].value;

        }
    }
    $.post( "clubs/add_club", {'club_data':JSON.stringify(clubObj)}, function() {
      console.log( "successfully requested to add club" );
      })
      .done(function(data) {
        if (data.success == false) {
            window.alert(data.message);
        } else {
            closeClubModal();
        }
      })
      .fail(function(err) {
        console.log(err);
      });
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