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

function deleteCoordinator(username) {
    var deleteCoordinator = window.confirm('Are you sure you want to delete the coordinator ' + username + '?');
    if (deleteCoordinator) {
        $.post( "coordinators/delete_coordinator", {'username':username}, function() {
            console.log( "successfully requested to delete coordinator" );
        })
            .done(function(data) {
                if (data.success == false) {
                    window.alert(data.error);
                } else {
                    console.log("successfully deleted coordinator");
                    window.location.reload();
                }
            })
    }

}