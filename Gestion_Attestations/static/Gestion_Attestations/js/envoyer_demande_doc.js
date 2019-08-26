$("#demande-doc-Modal").on('show.bs.modal',function(e) {
    let type_demande = $(e.relatedTarget).data("value");
    let matricule = $(e.relatedTarget).data("matricule");
    console.log(matricule);
    let confirm_modal_button = $("#confirm-demande-doc");
    window.url = confirm_modal_button.data("url");
    console.log(window.url);
    if(type_demande === 'domiciliation') $("#demande-doc-Modal .modal-body").text("Selectionnez \"Confirmer\" si vous êtes sûr de l'envoi de votre demande de "+type_demande);
    else $("#demande-doc-Modal .modal-body").text("Selectionnez \"Confirmer\" si vous êtes sûr de l'envoi de votre demande d'attestation de "+type_demande);
    confirm_modal_button.val(type_demande);
    if(matricule !== ''){
       window.url = $(e.relatedTarget).data("url");
    }
});

$("#confirm-demande-doc").click(function(e) {
    e.preventDefault();
    console.log("test");
    $('#demande-doc-Modal').modal('hide');
    let csrf = window.CSRF_TOKEN;
    if(window.url === undefined){
        console.log("TESTSSGDJDSMK");
        window.url = $(this).data('url');
    }
    let type_demande = $(this).val();
    $.ajax({
        type: 'POST',
        url: url,
        data:{
            'type_demande': type_demande,
            csrfmiddlewaretoken: csrf,
        },
        success: function(result) {
            if(type_demande === 'domiciliation') swal("Succès","Demande de "+type_demande+" envoyée avec succès","success");
            else swal("Succès","Demande d'attestation de "+type_demande+" envoyée avec succès","success");

        },
        error: function(result) {
           if(type_demande === 'domiciliation') swal("Echec","Demande de "+type_demande+" non envoyé","error");
           else swal("Echec","Demande d'attestation de "+type_demande+" non envoyé","error");
        }
    });
});


$('#notif-reply a').click(function (e) {
        if ($(this).attr('id') === 'accept-demande-doc') {
            let notif_id = $(this).val();
            $('#notification-detail-modal').modal('hide');
            let csrf = window.CSRF_TOKEN;
            $.ajax({
                url: $(this).data("url"),
                data: {
                    'notif_id': notif_id,
                    csrfmiddlewaretoken: csrf,
                },
                type: 'POST',
                datatype: 'json',
                success: function (result) {
                    swal("Succès", "Le document est prêt sous format PDF", "success");
                },
                error: function (result) {
                    swal("Echec", "Le document n'est pas prêt ", "error");
                }
            })
        }}
    );

$("#accept-demande-doc-type a").click(function (e) {
    let doc_id = $(e.currentTarget).data("value");
    let csrf = window.CSRF_TOKEN;
    console.log(doc_id);
    $.ajax({
        url: $(this).data("url"),
        data:{
            'doc_id':doc_id,
            csrfmiddlewaretoken: csrf,
        },
        type: 'POST',
        datatype : 'json',
        success: function(result) {
             swal("Succès","Le document est prêt sous format PDF","success");
        },
        error: function(result) {
            swal("Echec", "Le document n'est pas prêt ", "error");
        }
    })
});
