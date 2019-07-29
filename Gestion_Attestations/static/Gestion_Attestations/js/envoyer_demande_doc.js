$("#demande-doc-Modal").on('show.bs.modal',function(e) {
    type_demande = $(e.relatedTarget).data("value");
    if(type_demande == 'domiciliation') $("#demande-doc-Modal .modal-body").text("Selectionnez \"Confirmer\" si vous êtes sûr de l'envoi de votre demande de "+type_demande);
    else $("#demande-doc-Modal .modal-body").text("Selectionnez \"Confirmer\" si vous êtes sûr de l'envoi de votre demande d'attestation de "+type_demande);
    $("#confirm-demande-doc").val(type_demande);
});

$("#confirm-demande-doc").click(function(e) {
    e.preventDefault();
    type_demande = $(this).val();
    $.ajax({
        url: "attestations/demande_doc",
        data:{
            'type_demande': type_demande
        },
        success: function(result) {
            $('#demande-travail-Modal').modal('hide');
            if(type_demande == 'domiciliation') swal("Succès","Demande de "+type_demande+" envoyée avec succès","success");
            else swal("Succès","Demande d'attestation de "+type_demande+" envoyée avec succès","success");

        },
        error: function(result) {
            $("#demande-travail-Modal").modal('hide');
           if(type_demande == 'domiciliation') swal("Echec","Demande de "+type_demande+" non envoyé","error");
           else swal("Echec","Demande d'attestation de "+type_demande+" non envoyé","error");
        }
    });
});