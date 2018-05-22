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

function showEditClub(club_index) {
    $("#club-details-not-editing" + club_index).hide();
    $("#club-details-editing" + club_index).show();

    $("#club-details-header-sub" + club_index).hide();
    $("#club-details-edit" + club_index).show();
}

function editClub(club_name, club_index) {
    var clubForm = $("#club-details-form" + club_index).serializeArray();
    var clubObj = {'club_name':club_name}
    for (x in clubForm) {
        clubObj[clubForm[x].name] = clubForm[x].value;
    }
    $.post( "clubs/edit_club_address", {'club_data':JSON.stringify(clubObj)}, function() {
      console.log( "successfully requested to edit club address" );
      })
      .done(function(data) {
        if (data.success == false) {
            window.alert(data.error);
        } else {
            closeEditClub(club_index);
            $("#club-details-sub-address" + club_index).html(data.address);
        }
      })
      .fail(function(err) {
        console.log(err);
      });

}

function closeEditClub(club_index) {
    $("#club-details-not-editing" + club_index).show();
    $("#club-details-editing" + club_index).hide();

    $("#club-details-header-sub" + club_index).show();
    $("#club-details-edit" + club_index).hide();
}

function deleteClub(club_name) {
    var delete_club = window.confirm('Are you sure you want to delete this club?');
    if (delete_club) {
        $.post( "clubs/delete_club", {'club_name':club_name}, function() {
          console.log( "successfully requested to delete club" );
          })
          .done(function(data) {
            if (data.success == false) {
                window.alert(data.error);
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

function addClubCoordEdit(club_name) {
    username = window.prompt("Please enter the username of the coordinator");
    if (username != null) {
        $.post( "clubs/add_coordinator", {'username':username, 'club_name':club_name}, function() {
          console.log( "successfully requested to add coordinator to club" );
          })
          .done(function(data) {
            if (data.success == false) {
                window.alert(data.error);
            } else {
                window.alert('Success!')
                window.location.reload();
            }
          })
          .fail(function(err) {
            console.log(err);
          });
    }
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
            window.alert(data.error);
        } else {
            closeClubModal();
            window.location.reload();
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