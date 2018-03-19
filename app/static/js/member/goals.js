function toggleProofs(id) {
    var proofs_list = $("#" + id);
    if (proofs_list.is(":hidden")) {
        proofs_list.show("fast");
    } else {
        proofs_list.slideUp();
    }
}

function openProofModal(text, documentName) {
    $("#proofModal").modal('show');
    $("#upload_proof_name").html(text);
}

function closeProofModal() {
    $("#proofModal").modal('hide');
}

function saveProof() {
    closeProofModal();
}