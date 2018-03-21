function openGoalModal() {

}

function editGoal() {
    window.alert("Sorry, this feature hasn't been implemented yet");
}

function searchGoals() {
    window.alert("Sorry, this feature hasn't been implemented yet");
}

function filterGoals() {
    window.alert("Sorry, this feature hasn't been implemented yet");
}

function closeGoalModal() {
    $("#goalModal").modal('hide');
}

function saveGoalModal() {
    $("#goalModal").modal('hide');
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