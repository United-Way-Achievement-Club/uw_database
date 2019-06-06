$(document).ready(function() {
    var location = window.location.pathname.split("/")[2];
});

function featureNotImplemented() {
    window.alert("Sorry! This feature hasn't been implemented yet");
}

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
    $.post( "/coordinator/edit_profile", {'user_data':JSON.stringify(profileObj)}, function() {
      console.log( "successfully requested profile updates" );
      })
      .done(function(data) {
        $("#coordinator-profile").html(data);
      })
      .fail(function(err) {
        console.log(err);
      });
}

function addPhoneNumber() {
    if ($(".profile-phone-number").length >= 3) {
        window.alert("Users can add up to 3 phone numbers");
    } else {
        $("#profile-phone-numbers").append('<input name="phone_number" type="tel" class="profile-phone-number col-sm-10 uw-input profile-input input input-sm">');
    }
}

function openEditPictureModal() {
    $("#editPicture").modal("show");
}

function closeModal() {
    $("#editPicture").modal("hide");
    $("#profile-pic").val(null);
    $("#show-profile-img").cropper('destroy');
    $("#show-profile-img").attr('src', "#");
    $("#crop-success-button").hide();
    $("#coordinator-profile-pic").attr('src', DEFAULT_PIC_LOCATION);
}

function savePicture() {
    $("#show-profile-img").cropper('getCroppedCanvas').toBlob(function (blob) {
        var formData = new FormData();
        formData.append('profile_picture', blob);
        $.ajax('/coordinator/edit_profile_picture', {
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
              closeModal();
              $("#coordinator-profile").html(data);
            },
            error: function () {
              window.alert('Error uploading image');
            }
        });
    }, 'image/jpeg');
}

// when the crop button is clicked, get the cropped canvas and save it to
// local storage as a data URI. Destroy the cropper and hide the crop button.
function cropImage() {
    var cropped = $("#show-profile-img").cropper('getCroppedCanvas').toDataURL('image/jpeg', 0.8);
    $("#coordinator-profile-pic").attr('src', cropped);
}

// when an image is uploaded, read in the url of the image and put it into the cropper
// display the cropper and the crop button
function readURL(input) {
    $("#show-profile-img").cropper('destroy');
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
        $('#show-profile-img').attr('src', e.target.result);
        $('#show-profile-img').cropper({
          aspectRatio: 10 / 10,
          scalable: false,
          zoomOnTouch: false,
          zoomable:false
        });
    }
        reader.readAsDataURL(input.files[0]);
        $("#crop-success-button").show();
    }
}

// Functions for sorting Coordinators
    // Goal is to have one function that toggles between -1 and 1 pairing
    function sortZA() {
        // alert("Sort triggered.");
        $('.coordinators-list-item').sort(function(a, b) {
            if (a.textContent < b.textContent) {
              return -1;
            } else {
              return 1;
            }
          }).appendTo('.coordinators-list-items');
    };
    
    function sortAZ() {
        // alert("Sort triggered.");
        $('.coordinators-list-item').sort(function(a, b) {
            if (a.textContent < b.textContent) {
              return 1;
            } else {
              return -1;
            }
          }).appendTo('.coordinators-list-items');
    };

// Search for Coordinator
    function search() {
        var input, filter, li, a, txtValue;
        input = document.getElementById("searchInput");
        filter = input.value;
        li = $('.coordinators-list-item');
        for (i = 0; i < li.length; i++) {
            a = li[i].getElementsByClassName("coordinators-list-item-wrapper")[1];
            txtValue = a.textContent || a.innerText;
            anyCase = txtValue.toLowerCase();
            if (anyCase.indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }