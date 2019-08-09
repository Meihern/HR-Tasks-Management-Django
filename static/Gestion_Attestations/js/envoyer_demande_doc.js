$("#demande-doc-Modal").on('show.bs.modal',function(e) {
    type_demande = $(e.relatedTarget).data("value");
    if(type_demande == 'domiciliation') $("#demande-doc-Modal .modal-body").text("Selectionnez \"Confirmer\" si vous êtes sûr de l'envoi de votre demande de "+type_demande);
    else $("#demande-doc-Modal .modal-body").text("Selectionnez \"Confirmer\" si vous êtes sûr de l'envoi de votre demande d'attestation de "+type_demande);
    $("#confirm-demande-doc").val(type_demande);
});

$("#confirm-demande-doc").click(function(e) {
    e.preventDefault();
    type_demande = $(this).val();
    $('#demande-doc-Modal').modal('hide');
    $.ajax({
        url: $(this).data("url"),
        data:{
            'type_demande': type_demande,
        },
        success: function(result) {
            if(type_demande == 'domiciliation') swal("Succès","Demande de "+type_demande+" envoyée avec succès","success");
            else swal("Succès","Demande d'attestation de "+type_demande+" envoyée avec succès","success");

        },
        error: function(result) {
           if(type_demande == 'domiciliation') swal("Echec","Demande de "+type_demande+" non envoyé","error");
           else swal("Echec","Demande d'attestation de "+type_demande+" non envoyé","error");
        }
    });
});

$("#accept-demande-doc").click(function (e) {
    let notif_id = $(this).val();
    $('#notification-detail-modal').modal('hide');
    $.ajax({
        url: $(this).data("url"),
        data:{
            'notif_id': notif_id,
        },
        type: 'GET',
        datatype : 'json',
        success: function(result) {
             swal("Succès","Le document est prêt sous format PDF","success");
        },
        error: function(result) {
            swal("Echec", "Le document n'est pas prêt ", "error");
        }
    })
});

$("#accept-demande-doc-type a").click(function (e) {
    let doc_id = $(e.currentTarget).data("value");
    $.ajax({
        url: $(this).data("url"),
        data:{
            'doc_id':doc_id,
        },
        type: 'GET',
        datatype : 'json',
        success: function(result) {
             swal("Succès","Le document est prêt sous format PDF","success");
        },
        error: function(result) {
            swal("Echec", "Le document n'est pas prêt ", "error");
        }
    })
});
