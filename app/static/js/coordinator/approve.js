/**
 * Set the status of a proof based on input from coordinator.
 * Communicate with the server to update the proof status in
 * the database.
 * @param username member's username
 * @param proof_name name of the proof
 * @param step_name name of the step
 * @param status status (approved, denied)
 */
function set_document_status(username, proof_name, step_name, status) {
    prompt_text = status == "approved" ? "(optional) Reason for approval" : "Reason for denial";
    reason = window.prompt(prompt_text, "No reason entered");
    if (reason != null) {
        $.post( "approve/set_document_status", {'username':username, 'proof_name':proof_name, 'step_name':step_name, 'reason':reason, 'status':status}, function() {
          console.log( "successfully requested to approve proof" );
          })
          .done(function(data) {
            if (data.success == false) {
                window.alert(data.error);
            } else {
                window.alert('Success!')
                window.location.reload();
            }
          })
          .fail(function(err) {
            console.log(err);
          });
    }
}

/**
 * download a file (file found in an s3 link)
 * @param link the link to the file
 */
function download(link) {
    window.open(link, "_blank");
}