function set_document_status(username, proof_name, step_name, goal_name, status) {
    prompt_text = status == "approved" ? "(optional) Reason for approval" : "Reason for denial";
    reason = window.prompt(prompt_text, "No reason entered");
    if (reason != null) {
        $.post( "approve/set_document_status", {'username':username, 'proof_name':proof_name, 'step_name':step_name, 'goal_name':goal_name, 'reason':reason, 'status':status}, function() {
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

function download(link) {
    window.open(link, "_blank");
}