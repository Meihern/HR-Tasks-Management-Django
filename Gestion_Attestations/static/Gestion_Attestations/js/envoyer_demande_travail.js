$("#send-demande-travail").click(function(e) {
    e.preventDefault();
    $.ajax({
        url: "attestations/demande_travail",
        success: function(result) {
            $('#demande-travail-Modal').modal('hide');
            swal("Succès","Demande d'attestation de travail envoyée avec succès","success");
        },
        error: function(result) {
            $("#demande-travail-Modal").modal('hide');
            swal("Echec","Demande d'attestation de travail non envoyé","error");
        }
    });
});