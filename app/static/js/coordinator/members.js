$(document).ready(function() {
    $("#memberModalLabel").modal('hide');
    sessionStorage.currentPage = "general";
    sessionStorage.profilePicIsDataURI = false;
    sessionStorage.profile_picture = '/static/images/profile_pictures/default_profile_pic.png'
});


// close member modal and clear all fields in the general form
function closeModal() {
    sessionStorage.profilePicIsDataURI = false;
    sessionStorage.profile_picture = '/static/images/profile_pictures/default_profile_pic.png'
    sessionStorage.currentPage = "general";
    $("#profile-pic").val(null);
    $("#show-profile-img").cropper('destroy');
    $("#show-profile-img").attr('src', "#");
    $("#crop-success-button").hide();
    $("#member-profile-pic").attr('src', '/static/images/profile_pictures/default_profile_pic.png');
    $.post( "members/clear_new_member", function() {
      console.log( "successfully requested clear session" );
      })
      .done(function(data) {
        console.log( "successfully cleared session" );
        $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
        $("#general").addClass("member-modal-nav-item-active");
        $("#member-modal-body-component").html(data);
      })
      .fail(function() {
        console.log( "error clearing session" );
      })
      .always(function() {
        console.log( "clearing session..." );
      });
}

// save new member, send profile pic info to the server
function saveModal() {
    saveMemberToStorage(sessionStorage.currentPage);
    var profile_pic_blob;
    var profile_pic_type;
    if (sessionStorage.profilePicIsDataURI === 'true') {
        profile_pic_blob = dataURItoBlob(sessionStorage.profile_picture);
        profile_pic_type = "blob";
    } else {
        profile_pic_blob = sessionStorage.profile_picture;
        profile_pic_type = "saved_file";
    }
    var form_data = new FormData();
    form_data.append('profile_picture', profile_pic_blob)
    form_data.append('profile_pic_type', profile_pic_type)
    $.ajax('members/create_member', {
        method: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        success: function () {
          console.log('Create new member success');
          closeModal();
        },
        error: function () {
          window.alert('Error creating new member');
        }
    });
}

// change page on member modal. Save info from the current page, send to server to temporarily save
// in session, then go to new page
function memberModalChange(e) {
    var id = $(e).attr("id");
    var memberData = saveMemberToStorage(sessionStorage.currentPage);
    $.post( "members/update", {'key':sessionStorage.currentPage,'data':JSON.stringify(memberData),'next_page':id}, function() {
      console.log( "successfully requested html for modal change" );
      })
      .done(function(data) {
        console.log( "successfully received html for modal change" );
        $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
        $(e).addClass("member-modal-nav-item-active");
        $("#member-modal-body-component").html(data);
        sessionStorage.currentPage = id;
        if (id == "general") {
            $("#member-profile-pic").attr('src', sessionStorage.profile_picture);
        }
      })
      .fail(function() {
        console.log( "error receiving html for modal change" );
      })
      .always(function() {
        console.log( "retrieving modal change html" );
      });
}

// determine which page needs to be saved to storage
function saveMemberToStorage(page) {
    var updateMember;
    if (page == 'general') {
        updateMember = saveGeneral();
    } else if (page == 'enrollment_form') {
        updateMember = saveEnrollmentForm();
    } else if (page == 'demographic_data') {
        updateMember = saveDemographicData();
    } else if (page == 'self_sufficiency_matrix') {
        updateMember = saveSelfSufficiencyMatrix();
    } else if (page == 'self_efficacy_quiz') {
        updateMember = saveSelfEfficacyQuiz();
    }
    return updateMember;
}

// save the general form
function saveGeneral() {
    var generalObj = {};
    var generalValues = $("#general-form").serializeArray();
    for (v in generalValues) {
        generalObj[generalValues[v].name] = generalValues[v].value;
    }
    return generalObj;
}

// save the enrollment form
function saveEnrollmentForm() {
    var enrollementFormObj = {};
    var enrollmentValues = $("#enrollment-form").serializeArray();
    console.log(enrollmentValues);
    return enrollementFormObj;
}

// save the demographic data form
function saveDemographicData() {
    var demographicDataObj = {};
    return demographicDataObj;
}

// save the self sufficiency matrix form
function saveSelfSufficiencyMatrix() {
    var selfSufficiencyObj = {};
    return selfSufficiencyObj;
}

// save the self efficacy quiz form
function saveSelfEfficacyQuiz() {
    var selfEfficacyObj = {};
    return selfEfficacyObj;
}

// convert a data URI to a blob to send to the server
function dataURItoBlob(dataURI) {
  dataURI = dataURI.replace(/\s/g, '');
  // convert base64 to raw binary data held in a string
  // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
  var byteString = atob(dataURI.split(',')[1]);

  // separate out the mime component
  var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]

  // write the bytes of the string to an ArrayBuffer
  var ab = new ArrayBuffer(byteString.length);

  // create a view into the buffer
  var ia = new Uint8Array(ab);

  // set the bytes of the buffer to the correct values
  for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
  }

  // write the ArrayBuffer to a blob, and you're done
  var blob = new Blob([ab], {type: mimeString});
  return blob;

}

// ===================================== general ===============================================

// when the crop button is clicked, get the cropped canvas and save it to
// local storage as a data URI. Destroy the cropper and hide the crop button.
function cropImage() {
    var cropped = $("#show-profile-img").cropper('getCroppedCanvas').toDataURL('image/jpeg', 0.8);
    $("#member-profile-pic").attr('src', cropped);
    sessionStorage.profilePicIsDataURI = true;
    sessionStorage.profile_picture = cropped;
    $("#show-profile-img").cropper('destroy');
    $("#show-profile-img").attr('src', "#");
    $("#crop-success-button").hide();
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

// ===================================== enrollment form ===============================================

function addPhoneNumber() {
    $("#member-phone-numbers").append('<div class="form-group row"><input name="phone_numbers" type="tel" placeholder="Phone Number" class="input input-sm uw-input col-sm-4 phone-number"><button onclick="removeNum(this)" class="btn btn-sm uw-button"><span class="glyphicon glyphicon-remove"></span></button></div>');
}

function removeNum(e) {
    var parent = $(e).parent();
    $(parent).remove();
}

function addChild() {
    var child = $("#member-children-table .member-child:first-child").html();
    var child_num = parseInt($("#member-children-table .member-child:last-child .child-num").html());
    $("#member-children-table").append('<tr class="member-child">' + child + '</tr>');
    $("#member-children-table .member-child:last-child .child-num").html(child_num + 1);
}