function openGoalModal() {

}

// parameter must be an array of strings
function editGoal(goal_name) {
    $.post( "goals/edit_goal_modal", {'goal_name':goal_name}, function() {
          console.log( "successfully requested to edit goal" );
          })
          .done(function(data) {
            $("#edit_goal_modal").html(data);
            $("#goalEditModal").modal('show');
          })
          .fail(function(err) {
            console.log(err);
          });
}

function deleteGoal() {
    window.alert("Sorry, this feature hasn't been implemented yet");
}

function searchGoals() {
    window.alert("Sorry, this feature hasn't been implemented yet");
}

function filterGoals() {
    window.alert("Sorry, this feature hasn't been implemented yet");
}

function closeGoalModal() {
    $(".goal-modal-body input").val("");
    $(".goal-modal-body textarea").val("");
    $("#goalModal").modal('hide');
}

function closeEditGoalModal() {
    $("#goalEditModal").modal('hide');
}

function updateGoalModal(goal_name) {
    var goalObj = {"steps":[]};
    var general_form = $("#edit-general-form").serializeArray();
    //for (value in general_form) {
    //    goalObj[general_form[value].name] = general_form[value].value;
    //}
    goalObj['goal_name'] = goal_name;
    goalObj.steps.push(createProofObject("edit-step1-form"));
    goalObj.steps.push(createProofObject("edit-step2-form"));
    goalObj.steps.push(createProofObject("edit-step3-form"));
    $.post( "goals/edit_goal", {'goal':JSON.stringify(goalObj)}, function() {
      console.log( "successfully requested to edit goal" );
      })
      .done(function(data) {
        if (data.success == false) {
            window.alert(data.message);
        } else {
            closeEditGoalModal();
        }
      })
      .fail(function(err) {
        console.log(err);
      });
}

function saveGoalModal() {
    var goalObj = {"steps":[]};
    var general_form = $("#general-form").serializeArray();
    for (value in general_form) {
        goalObj[general_form[value].name] = general_form[value].value;
    }
    goalObj.steps.push(createProofObject("step1-form"));
    goalObj.steps.push(createProofObject("step2-form"));
    goalObj.steps.push(createProofObject("step3-form"));
    $.post( "goals/add_goal", {'goal':JSON.stringify(goalObj)}, function() {
      console.log( "successfully requested to add goal" );
      })
      .done(function(data) {
        if (data.success == false) {
            window.alert(data.message);
        } else {
            closeGoalModal();
        }
      })
      .fail(function(err) {
        console.log(err);
      });
}

function createProofObject(form) {
    var form_name = $("#" + form).serializeArray();
    var formObj = {"step_name":form_name[0].value,"proofs":[]}
    var createObj = true;
    var proofs = {};
    for (var y = 1; y < form_name.length; y++) {
        proofs[form_name[y].name] = form_name[y].value;
        if (createObj) {
            createObj = false;
        } else {
            formObj.proofs.push(proofs);
            proofs = {};
            createObj = true;
        }
    }
    return formObj;
}

function addProof(step) {
    var html = $("#proof-html-hide").html();
    $("#" + step).append(html);
}

// remove proof
function removeProof(e) {
    var parent = $(e).parent();
    var grand_parent = $(parent).parent();
    $(grand_parent).remove();
}

function showStep(e, index, stepName) {
    $('.goal-steps-nav-item' + index).removeClass('goal-steps-nav-item-active');
    $(e).addClass('goal-steps-nav-item-active');
    $('.goal-proofs' + index).addClass('goal-proofs-hide');
    $('#' + stepName).removeClass('goal-proofs-hide');
}