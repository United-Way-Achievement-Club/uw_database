function editProfile() {
    $("#view_profile").hide();
    $("#edit_profile").show();
    $("#profile-edit-ic").hide();
}

function saveProfile() {
    var profileObj = {"phone_numbers":[]}
    var profileData = $("#edit-profile-form").serializeArray();
    for (v in profileData) {
        if (profileData[v].name === "phone_number") {
            if (profileData[v].value != "") {
                profileObj.phone_numbers.push(profileData[v].value);
            }
        } else {
            profileObj[profileData[v].name] = profileData[v].value;
        }
    }
    $.post( "/member/edit_profile", {'member_data':JSON.stringify(profileObj)}, function() {
      console.log( "successfully requested profile updates" );
      })
      .done(function(data) {
        $("#member-profile").html(data);
      })
      .fail(function(err) {
        console.log(err);
      });
}

function addPhoneNumber() {
    if ($(".profile-phone-number").length >= 3) {
        window.alert("Members can add up to 3 phone numbers");
    } else {
        $("#profile-phone-numbers").append('<input name="phone_number" type="tel" class="profile-phone-number col-sm-10 uw-input profile-input input input-sm">');
    }
}