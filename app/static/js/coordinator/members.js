$(document).ready(function() {
    $("#memberModalLabel").modal('hide');
    localStorage.newMember = JSON.stringify({"general":{}, "enrollment_form":{}, "demographic_data":{}, "self_sufficiency_matrix":{}, "self_efficacy_quiz":{}, "goals":{}});
    localStorage.currentPage = "general";
    localStorage.profilePicIsDataURI = false;
    sessionStorage.profile_picture = '/static/images/profile_pictures/default_profile_pic.png'
});

function closeModal() {
    localStorage.profilePicIsDataURI = false;
    sessionStorage.profile_picture = '/static/images/profile_pictures/default_profile_pic.png'
    localStorage.newMember = JSON.stringify({"general":{}, "enrollment_form":{}, "demographic_data":{}, "self_sufficiency_matrix":{}, "self_efficacy_quiz":{}, "goals":{}});
    localStorage.currentPage = "general";
    $("#profile-pic").val(null);
    $("#show-profile-img").cropper('destroy');
    $("#show-profile-img").attr('src', "#");
    $("#crop-success-button").hide();
    $("#member-profile-pic").attr('src', '/static/images/profile_pictures/default_profile_pic.png');
    $("#general-form")[0].reset();
}

function saveModal() {
    saveMemberToStorage(localStorage.currentPage);
    var profile_pic_blob;
    var profile_pic_type;
    if (localStorage.profilePicIsDataURI === 'true') {
        profile_pic_blob = dataURItoBlob(sessionStorage.profile_picture);
        profile_pic_type = "blob";
    } else {
        profile_pic_blob = sessionStorage.profile_picture;
        profile_pic_type = "saved_file";
    }

    var form_data = new FormData();
    form_data.append('profile_picture', profile_pic_blob)
    form_data.append('profile_pic_type', profile_pic_type)
    form_data.append('new_member', localStorage.newMember)
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

function memberModalChange(e) {
    var newMember = JSON.parse(localStorage.newMember);
    var id = $(e).attr("id");
    saveMemberToStorage(localStorage.currentPage);
    localStorage.currentPage = id;
    $.post( "members/" + id, newMember[id], function() {
      console.log( "successfully requested html for modal change" );
      })
      .done(function(data) {
        console.log( "successfully received html for modal change" );
        $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
        $(e).addClass("member-modal-nav-item-active");
        $("#member-modal-body-component").html(data);
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

function saveMemberToStorage(page) {
    var updateMember;
    var newMember = JSON.parse(localStorage.newMember);
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
    newMember[page] = updateMember;
    localStorage.newMember = JSON.stringify(newMember);
}

function saveGeneral() {
    var generalObj = {};
    var generalValues = $("#general-form").serializeArray();
    for (v in generalValues) {
        generalObj[generalValues[v].name] = generalValues[v].value;
    }
    return generalObj;
}

function saveEnrollmentForm() {
    var enrollementFormObj = {};
    return enrollementFormObj;
}

function saveSelfSufficiencyMatrix() {
    var selfSufficiencyObj = {};
    return selfSufficiencyObj;
}

function saveSelfEfficacyQuiz() {
    var selfEfficacyObj = {};
    return selfEfficacyObj;
}

function cropImage() {
    var cropped = $("#show-profile-img").cropper('getCroppedCanvas').toDataURL('image/jpeg', 0.8);
    $("#member-profile-pic").attr('src', cropped);
    localStorage.profilePicIsDataURI = true;
    sessionStorage.profile_picture = cropped;
}

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