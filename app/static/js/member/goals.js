function toggleProofs(id) {
    var proofs_list = $("#" + id);
    if (proofs_list.is(":hidden")) {
        proofs_list.show("slow");
    } else {
        proofs_list.slideUp();
    }
}