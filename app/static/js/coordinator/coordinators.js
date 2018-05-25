function closeCoordinatorModal() {
    $("#new-coordinator input").val("");
    $("#coordinatorModal").modal('hide');
}

function saveCoordinator() {
    $("#new-coordinator").submit();
    closeCoordinatorModal();
}