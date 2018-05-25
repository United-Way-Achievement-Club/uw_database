function toggleProofs(id) {
    var proofs_list = $("#" + id);
    if (proofs_list.is(":hidden")) {
        proofs_list.show("fast");
    } else {
        proofs_list.slideUp();
    }
}

function openProofModal(text, step_name, documentName) {
    $("#proofModal").modal('show');
    $("#upload_proof_name").html(text);
    $("#proof_file").val(null);
    $("#proof_name").val(text);
    $("#step_name").val(step_name);
}

function closeProofModal() {
    $("#proofModal").modal('hide');
}

function saveProof() {
    $("#upload-proof-form").submit();
    closeProofModal();
}