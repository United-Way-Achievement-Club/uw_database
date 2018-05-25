function closeCoordinatorModal() {
    $("#new-coordinator input").val("");
    $("#coordinatorModal").modal('hide');
}

function saveCoordinator() {
    var proceed = window.confirm('Proceed with adding coordinator? We will email the new coordinator his/her username with a generated password.');
    if (proceed) {
        $("#new-coordinator").submit();
        closeCoordinatorModal();
    }
}