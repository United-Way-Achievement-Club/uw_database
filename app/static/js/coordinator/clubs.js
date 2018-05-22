function showClubDetails(club) {
    $(".club-details").hide();
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

function editClub(club_index) {
    window.alert('Sorry, this feature has not been implemented yet!');
}

function deleteClub(club_name) {
    var delete_club = window.confirm('Are you sure you want to delete this club?');
    if (delete_club) {
        $.post( "clubs/delete_club", {'club_name':club_name}, function() {
          console.log( "successfully requested to delete club" );
          })
          .done(function(data) {
            if (data.success == false) {
                window.alert(data.message);
            } else {
                window.location.reload();
            }
          })
          .fail(function(err) {
            console.log(err);
          });
    }
}

function addPhoto() {
    window.alert('Sorry, this feature has not been implemented yet!');
}

function addClubCoordEdit() {
    window.alert('Sorry, this feature has not been implemented yet!');
}

function addClubMemberEdit() {
    window.alert('Sorry, this feature has not been implemented yet! You can add a member by going to the Members page, editing the new members profile, and setting his/her club to this one.')
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