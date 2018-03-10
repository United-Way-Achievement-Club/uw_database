const DEFAULT_PIC_LOCATION = '/static/images/profile_pictures/default_profile_pic.png'

// set the current page and storage options
$(document).ready(function() {
    sessionStorage.currentPage = "general";
    sessionStorage.profilePicIsDataURI = false;
    sessionStorage.profile_picture = DEFAULT_PIC_LOCATION;

});



// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};

// hide all previous form alerts
function hideAlerts() {
    $(".form_alert").hide();
}

function emptyModal() {
    $("#memberModal").modal('hide');
    sessionStorage.profilePicIsDataURI = false;
    sessionStorage.profile_picture = DEFAULT_PIC_LOCATION;
    sessionStorage.currentPage = "general";
    $("#profile-pic").val(null);
    $("#show-profile-img").cropper('destroy');
    $("#show-profile-img").attr('src', "#");
    $("#crop-success-button").hide();
    $("#member-profile-pic").attr('src', DEFAULT_PIC_LOCATION);
    $("#self-sufficiency-score").html('19');
    $("#self-efficacy-score").html('19');
    $("#self_sufficiency_matrix_dropdown .member-modal-nav-item-dropdown").not("#self_sufficiency_matrix_dropdown .member-modal-nav-item-dropdown:first").remove();
    $("#self_efficacy_quiz_dropdown .member-modal-nav-item-dropdown").not("#self_efficacy_quiz_dropdown .member-modal-nav-item-dropdown:first").remove();
    if (!$("#self_sufficiency_matrix_dropdown").is(":hidden")) {
        $("#self_sufficiency_matrix_dropdown").hide();
        $(".member-modal-dropdown-active").removeClass("member-modal-dropdown-active");
        $(".member-modal-nav-item-dropdown-active").removeClass("member-modal-nav-item-dropdown-active");
        $("#self_sufficiency_matrix_ic").css({"transform": "rotate(" + 0 + "deg) translateY(-1px)"});
    }
    if (!$("#self_efficacy_quiz_dropdown").is(":hidden")) {
        $("#self_efficacy_quiz_dropdown").hide();
        $(".member-modal-dropdown-active").removeClass("member-modal-dropdown-active");
        $(".member-modal-nav-item-dropdown-active").removeClass("member-modal-nav-item-dropdown-active");
        $("#self_efficacy_quiz_ic").css({"transform": "rotate(" + 0 + "deg) translateY(-1px)"});
    }
}

// close member modal and clear all fields in the general form
function closeModal() {
    $.post( "members/clear_new_member", function() {
      console.log( "successfully requested clear session" );
      })
      .done(function(data) {
        console.log( "successfully cleared session" );
        emptyModal();
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
    var newData = saveMemberToStorage(sessionStorage.currentPage);
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
    form_data.append('profile_picture', profile_pic_blob);
    form_data.append('profile_pic_type', profile_pic_type);
    form_data.append('current_page',sessionStorage.currentPage);
    form_data.append('new_data', JSON.stringify(newData));
    $.ajax('members/create_member', {
        method: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (data) {
          if (data.success == true) {
            console.log('Create new member success');
            emptyModal();
            $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
            $("#general").addClass("member-modal-nav-item-active");
            $("#member-modal-body-component").html(data.template);
          } else {
            $(".form_alert").hide();
            $("#" + data.form + "_alert").show();
            window.alert(data.error_message);
          }
        },
        error: function () {
          window.alert('Error creating new member');
        }
    });
}

// close the modal in edit mode
function closeEditModal() {
    $.post( "members/clear_edit_member", function() {
      console.log( "successfully closed modal" );
      })
      .done(function(data) {
        emptyModal();
        $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
        $("#general").addClass("member-modal-nav-item-active");
        $("#member-modal-wrapper").html(data);
        $("body").removeClass("modal-open");
        $('.modal-backdrop').remove();
      })
      .fail(function() {
        console.log( "error clearing edit member session..." );
      })
      .always(function() {
        console.log( "closing modal" );
      });
}

// save the modal in edit mode
function saveEditModal() {
    var newData = saveMemberToStorage(sessionStorage.currentPage);
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
    form_data.append('profile_picture', profile_pic_blob);
    form_data.append('profile_pic_type', profile_pic_type);
    form_data.append('current_page',sessionStorage.currentPage);
    form_data.append('new_data', JSON.stringify(newData));
    $.ajax('members/update_member', {
        method: "POST",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (data) {
          if (data.success == true) {
            console.log('Update member success');
            emptyModal();
            $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
            $("#general").addClass("member-modal-nav-item-active");
            $("#member-modal-wrapper").html(data.template);
            $("body").removeClass("modal-open");
            $('.modal-backdrop').remove();
          } else {
            $(".form_alert").hide();
            $("#" + data.form + "_alert").show();
            window.alert(data.error_message);

          }
        },
        error: function () {
          window.alert('Error creating new member');
        }
    });
}

function openEditModal(username) {
    $.post( "members/edit", {'username':username}, function() {
      console.log( "successfully requested to edit user " + username );
      })
      .done(function(data) {
        console.log( "successfully opened edit user modal" );
        $("#member-modal-wrapper").html(data);
        $("#memberModal").modal({backdrop: 'static', keyboard: false});
      })
      .fail(function() {
        console.log( "error opening modal..." );
      })
      .always(function() {
        console.log( "opening edit member modal" );
      });
}

// change page on member modal. Save info from the current page, send to server to temporarily save
// in session, then go to new page
function memberModalChange(e) {
    var id = $(e).attr("id");
    var memberData = saveMemberToStorage(sessionStorage.currentPage);
    if (id == "self_sufficiency_matrix" || id == "self_efficacy_quiz") {
        showDropdown(id + "_dropdown", id + "_ic");
    }
    $.post( "members/update", {'key':sessionStorage.currentPage,'data':JSON.stringify(memberData),'next_page':id}, function() {
      console.log( "successfully requested html for modal change" );
      })
      .done(function(data) {
        console.log( "successfully received html for modal change" );
        $(".member-modal-dropdown-active").removeClass("member-modal-dropdown-active");
        $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
        $(".member-modal-nav-item-dropdown-active").removeClass("member-modal-nav-item-dropdown-active");
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

function dropdownChange(e) {
    var id = $(e).attr("id");
    var memberData = saveMemberToStorage(sessionStorage.currentPage);
    var setActive = showDropdown(id + "_dropdown", id + "_ic");
    if (setActive) {
        $.post( "members/update", {'key':sessionStorage.currentPage,'data':JSON.stringify(memberData),'next_page':id}, function() {
          console.log( "successfully requested html for modal change" );
          })
          .done(function(data) {
            console.log( "successfully received html for modal change" );
            $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
            $(e).addClass("member-modal-nav-item-active");
            $("#member-modal-body-component").html(data);
            sessionStorage.currentPage = id;
          })
          .fail(function() {
            console.log( "error receiving html for modal change" );
          })
          .always(function() {
            console.log( "retrieving modal change html" );
          });
    }
}

function showDropdown(dropdownName, icName) {
    if ($("#" + dropdownName).is(":hidden")) {
        $("#" + dropdownName).slideDown("slow");
        $(".member-modal-dropdown-active").removeClass("member-modal-dropdown-active");
        $(".member-modal-nav-item-dropdown-active").removeClass("member-modal-nav-item-dropdown-active");
        $("#" + dropdownName).addClass("member-modal-dropdown-active");
        $("#" + dropdownName + " .member-modal-nav-item-dropdown:first-child").addClass("member-modal-nav-item-dropdown-active");
        $("#" + icName).css({"transform": "rotate(" + 90 + "deg) translateY(-1px)"});
        return true;
    } else {
        $("#" + dropdownName).slideUp();
        $("#" + icName).css({"transform": "rotate(" + 0 + "deg) translateY(-1px)"});
        return false;
    }
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
    } else if (page == 'goals') {
        updateMember = saveGoals();
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
// push the phone numbers to a list of phone numbers
// push information for children to a list of children, updating
// the child index each time the last child form field is reached
function saveEnrollmentForm() {
    var enrollmentFormObj = {"phone_numbers":[], "children":[{}]};
    var enrollmentValues = $("#enrollment-form").serializeArray();
    var childIndex = 0;
    for (v in enrollmentValues) {
            if (enrollmentValues[v].name === "phone_numbers") {
                enrollmentFormObj.phone_numbers.push(enrollmentValues[v].value)
            } else if (enrollmentValues[v].name.includes("child")) {
                enrollmentFormObj.children[childIndex][enrollmentValues[v].name] = enrollmentValues[v].value;
                if (enrollmentValues[v].name === "child_school" && v < enrollmentValues.length - 1) {
                    childIndex++;
                    enrollmentFormObj.children[childIndex] = {};
                }
            } else {
                enrollmentFormObj[enrollmentValues[v].name] = enrollmentValues[v].value;
            }
        }
    for (child in enrollmentFormObj.children) {
        if (child !== "remove" && checkBlankObject(enrollmentFormObj.children[child], "child_gender")) {
            enrollmentFormObj.children.remove(child);
        }
    }
    return enrollmentFormObj;
}

// save the demographic data form
function saveDemographicData() {
    var demographicDataObj = {"income_sources":[], "assets":[], "wars_served":[]};
    var demographicValues = $("#demographic-data-form").serializeArray();
    var medical_issues;
    for (v in demographicValues) {
        if (demographicValues[v].name === "income_sources") {
            demographicDataObj.income_sources.push(demographicValues[v].value);
        } else if (demographicValues[v].name === "assets") {
            demographicDataObj.assets.push(demographicValues[v].value);
        } else if (demographicValues[v].name === "wars_served") {
            demographicDataObj.wars_served.push(demographicValues[v].value);
        } else if (demographicValues[v].name === "medical_issues") {
            medical_issues = (demographicValues[v].value).split(",");
            for (issue in medical_issues) {
                if (!(typeof medical_issues[issue] === "function")) {
                    medical_issues[issue] = (medical_issues[issue]).trim();
                }
            }
            demographicDataObj['medical_issues'] = medical_issues
        } else {
            demographicDataObj[demographicValues[v].name] = demographicValues[v].value;
        }
    }
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

function saveGoals() {
    var goalsObj = {};
    // TODO: parse the values from the form and add to goalsObj
    return goalsObj;
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

// check if an object has only blank values
function checkBlankObject(obj, except) {
    for (v in obj) {
        if (obj[v] !== '' && v !== except) {
            return false;
        }
    }
    return true;
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

// add a new phone number field
function addPhoneNumber() {
    $("#member-phone-numbers").append('<div class="form-group row"><input name="phone_numbers" type="tel" placeholder="Phone Number" class="input input-sm uw-input col-sm-4 phone-number"><button onclick="removeNum(this)" class="btn btn-sm uw-button"><span class="glyphicon glyphicon-remove"></span></button></div>');
}

// remove phone number field
function removeNum(e) {
    var parent = $(e).parent();
    $(parent).remove();
}

// add a new child to table
function addChild() {
    var child = $("#member-children-table .member-child:first-child").html();
    var child_num = parseInt($("#member-children-table .member-child:last-child .child-num").html());
    $("#member-children-table").append('<tr class="member-child">' + child + '</tr>');
    $("#member-children-table .member-child:last-child .child-num").html(child_num + 1);
    $("#member-children-table .member-child:last-child input").val('');
}

// ===================================== self sufficiency matrix ===============================================

function changeScore() {
    var score = 0;
    $(".self-sufficiency-answer").each(function(i, obj) {
        score += parseInt($(obj).val());
    });
    $("#self-sufficiency-score").html(score);
}

function saveAssesment() {
    var selfSufficiencyValues = $("#self-sufficiency-matrix-form").serializeArray();
    var date;
    var answers = {};
    for (v in selfSufficiencyValues) {
        if (selfSufficiencyValues[v].name === 'date') {
            date = selfSufficiencyValues[v].value;
        } else {
            answers[selfSufficiencyValues[v].name] = selfSufficiencyValues[v].value;
        }
    }
    console.log(answers);
    console.log(date);
    if (date === undefined) {
        date = $("#date-header").html();
    }
    $.post( "members/save_self_sufficiency_matrix", {'date':date,'answers':JSON.stringify(answers)}, function() {
      console.log( "successfully requested html for modal change" );
      })
      .done(function(data) {
        if (data.success == false) {
            window.alert(data.error_message);
        } else {
            console.log( "successfully added self sufficiency matrix answer" );
            $("#member-modal-body-component").html(data);
            $("#self_sufficiency_matrix_dropdown").append('<div id="' + date + '" onclick="viewMatrix(this)" class="member-modal-nav-item-dropdown"><a><h5>' + date + '</h5></a></div>');
        }
        changeScore();
      })
      .fail(function(err) {
        console.log( "error adding self sufficiency matrix answer" );
        console.log(err);
      })
      .always(function() {
        console.log( "adding self sufficiency matrix answer" );
      });
}

function viewMatrix(e) {
    var id = $(e).attr("id");
    var date = $("#" + id + " a h5").html();
    var memberData = saveMemberToStorage(sessionStorage.currentPage);
    var currentPage = sessionStorage.currentPage;
    $.post( "members/self_sufficiency_matrix", {'date':date, 'key':currentPage, 'data':JSON.stringify(memberData)}, function() {
      console.log( "successfully requested html for modal change" );
      })
      .done(function(data) {
        console.log( "successfully viewing html for self sufficiency matrix" );
        $(".member-modal-nav-item-dropdown-active").removeClass('member-modal-nav-item-dropdown-active');
        $(e).addClass("member-modal-nav-item-dropdown-active");
        $("#member-modal-body-component").html(data);
        $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
        $(".member-modal-dropdown-active").removeClass('member-modal-dropdown-active');
        if (!$("#self_sufficiency_matrix").hasClass('member-modal-nav-item-active')) {
            $("#self_sufficiency_matrix").addClass('member-modal-nav-item-active');
        }
        if (!$("#self_sufficiency_matrix_dropdown").hasClass('member-modal-dropdown-active')) {
            $("#self_sufficiency_matrix_dropdown").addClass('member-modal-dropdown-active')
        }
        sessionStorage.currentPage = 'self_sufficiency_matrix';
        changeScore();

      })
      .fail(function(err) {
        console.log( "error viewing html for self sufficiency matrix" );
        console.log(err);
      })
      .always(function() {
        console.log( "getting html for self sufficiency matrix" );
      });
  }

 function removeAssesment(date) {
    $.post( "members/remove_self_sufficiency_matrix", {'date':date}, function() {
      console.log( "successfully requested to remove self sufficiency matrix" );
      })
      .done(function(data) {
        console.log( "successfully requested to remove self sufficiency matrix" );
        $("#member-modal-body-component").html(data);
        $("#self_sufficiency_matrix_dropdown .member-modal-nav-item-dropdown:first-child").addClass("member-modal-nav-item-dropdown-active");
        $("#" + date).remove();
        changeScore();

      })
      .fail(function(err) {
        console.log( "error viewing html for self sufficiency matrix" );
        console.log(err);
      })
      .always(function() {
        console.log( "getting html for self sufficiency matrix" );
      });
 }

 // ===================================== self efficacy quiz ===============================================


function changeQuizScore() {
    var score = 0;
    $(".self-efficacy-answer").each(function(i, obj) {
        score += parseInt($(obj).val());
    });
    $("#self-efficacy-score").html(score);
}

function saveQuiz() {
    var selfEfficacyValues = $("#self-efficacy-quiz-form").serializeArray();
    var date;
    var answers = {};
    for (v in selfEfficacyValues) {
        if (selfEfficacyValues[v].name === 'date') {
            date = selfEfficacyValues[v].value;
        } else {
            answers[selfEfficacyValues[v].name] = selfEfficacyValues[v].value;
        }
    }
    if (date === undefined) {
        date = $("#quiz-date-header").html();
    }
    $.post( "members/save_self_efficacy_quiz", {'date':date,'answers':JSON.stringify(answers)}, function() {
      console.log( "successfully requested html for modal change" );
      })
      .done(function(data) {
        if (data.success == false) {
            window.alert(data.error_message);
        } else {
            console.log( "successfully added self efficacy quiz answer" );
            $("#member-modal-body-component").html(data);
            $("#self_efficacy_quiz_dropdown").append('<div id="' + date + '" onclick="viewQuiz(this)" class="member-modal-nav-item-dropdown"><a><h5>' + date + '</h5></a></div>');
        }
        changeQuizScore();
      })
      .fail(function(err) {
        console.log( "error adding self efficacy quiz answer" );
        console.log(err);
      })
      .always(function() {
        console.log( "adding self efficacy quiz answer" );
      });
}

function viewQuiz(e) {
    var id = $(e).attr("id");
    var date = $("#" + id + " a h5").html();
    var memberData = saveMemberToStorage(sessionStorage.currentPage);
    var currentPage = sessionStorage.currentPage;
    $.post( "members/self_efficacy_quiz", {'date':date, 'key':currentPage, 'data':JSON.stringify(memberData)}, function() {
      console.log( "successfully requested html for modal change" );
      })
      .done(function(data) {
        console.log( "successfully viewing html for self sufficiency efficacy quiz" );
        $(".member-modal-nav-item-dropdown-active").removeClass('member-modal-nav-item-dropdown-active');
        $(e).addClass("member-modal-nav-item-dropdown-active");
        $("#member-modal-body-component").html(data);
        $(".member-modal-nav-item-active").removeClass("member-modal-nav-item-active");
        $(".member-modal-dropdown-active").removeClass('member-modal-dropdown-active');
        if (!$("#self_efficacy_quiz").hasClass('member-modal-nav-item-active')) {
            $("#self_efficacy_quiz").addClass('member-modal-nav-item-active');
        }
        if (!$("#self_efficacy_quiz_dropdown").hasClass('member-modal-dropdown-active')) {
            $("#self_efficacy_quiz_dropdown").addClass('member-modal-dropdown-active')
        }
        sessionStorage.currentPage = 'self_efficacy_quiz';
        changeQuizScore();

      })
      .fail(function(err) {
        console.log( "error viewing html for self efficacy quiz" );
        console.log(err);
      })
      .always(function() {
        console.log( "getting html for self efficacy quiz" );
      });
  }

 function removeQuiz(date) {
    $.post( "members/remove_self_efficacy_quiz", {'date':date}, function() {
      console.log( "successfully requested to remove self efficacy quiz" );
      })
      .done(function(data) {
        console.log( "successfully requested to remove self efficacy quiz" );
        $("#member-modal-body-component").html(data);
        $("#self_efficacy_quiz_dropdown .member-modal-nav-item-dropdown:first-child").addClass("member-modal-nav-item-dropdown-active");
        $("#" + date).remove();
        changeQuizScore();

      })
      .fail(function(err) {
        console.log( "error viewing html for self sufficiency matrix" );
        console.log(err);
      })
      .always(function() {
        console.log( "getting html for self sufficiency matrix" );
      });
 }