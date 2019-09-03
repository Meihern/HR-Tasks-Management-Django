$("#demande-doc-Modal").on('show.bs.modal',function(e) {
    let type_demande = $(e.relatedTarget).data("value");
    let matricule = $(e.relatedTarget).data("matricule");
    let confirm_modal_button = $("#confirm-demande-doc");
    window.url = confirm_modal_button.data("url");
    if(type_demande === 'domiciliation') $("#demande-doc-Modal .modal-body").text("Selectionnez \"Confirmer\" si vous êtes sûr de l'envoi de votre demande de "+type_demande);
    else $("#demande-doc-Modal .modal-body").text("Selectionnez \"Confirmer\" si vous êtes sûr de l'envoi de votre demande d'attestation de "+type_demande);
    confirm_modal_button.val(type_demande);
    if(matricule !== ''){
       window.url = $(e.relatedTarget).data("url");
    }
});

$("#confirm-demande-doc").click(function(e) {
    e.preventDefault();
    $('#demande-doc-Modal').modal('hide');
    let csrf = window.CSRF_TOKEN;
    if(window.url === undefined){
        window.url = $(this).data('url');
    }
    let type_demande = $(this).val();
    Swal.fire({
        title:'Attendez un instant !',
        text: "Votre demande est en cours d'envoi",
    });
    Swal.showLoading({
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        allowClickOutside: false,
    });
    $.ajax({
        type: 'POST',
        url: url,
        data:{
            'type_demande': type_demande,
            csrfmiddlewaretoken: csrf,
        },
        success: function(result) {
            Swal.close();
            if(type_demande === 'domiciliation') Swal.fire("Succès","Demande de "+type_demande+" envoyée avec succès","success");
            else Swal.fire("Succès","Demande d'attestation de "+type_demande+" envoyée avec succès","success");

        },
        error: function(result) {
            Swal.close();
           if(type_demande === 'domiciliation') Swal.fire("Echec","Demande de "+type_demande+" non envoyé","error");
           else Swal.fire("Echec","Demande d'attestation de "+type_demande+" non envoyé","error");
        }
    });
});


$('#notif-reply a').click(function (e) {
    e.preventDefault();
        if ($(this).attr('id') === 'accept-demande-doc') {
            let notif_id = $(this).val();
            let href = $(this).attr('href');
            $('#notification-detail-modal').modal('hide');
            let csrf = window.CSRF_TOKEN;
            Swal.fire({
        title:'Attendez un instant !',
        text: "Le document PDF est en cours de traitement",
         });

        Swal.showLoading({
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        allowClickOutside: false,
        });
            $.ajax({
                url: $(this).data("url"),
                data: {
                    'notif_id': notif_id,
                    csrfmiddlewaretoken: csrf,
                },
                type: 'POST',
                datatype: 'json',
                success: function (result) {
                    Swal.fire("Succès", "Le document est prêt sous format PDF", "success");
                    console.log(href);
                    window.open(href, '_blank');
                },
                error: function (result) {
                    Swal.fire("Echec", "Le document n'est pas prêt ", "error");
                }
            })
        }}
    );

$("#accept-demande-doc-type a").click(function (e) {
    e.preventDefault();
    let href = $(e.currentTarget).attr('href');
    let doc_id = $(e.currentTarget).data("value");
    let csrf = window.CSRF_TOKEN;
    Swal.fire({
        title:'Attendez un instant !',
        text: "Le document PDF est en cours de traitement",
         });

        Swal.showLoading({
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        allowClickOutside: false,
        });
    $.ajax({
        url: $(this).data("url"),
        data:{
            'doc_id':doc_id,
            csrfmiddlewaretoken: csrf,
        },
        type: 'POST',
        datatype : 'json',
        success: function(result) {
             Swal.close();
             Swal.fire("Succès","Le document est prêt sous format PDF","success");
             window.open(href, '_blank');
        },
        error: function(result) {
            Swal.close();
            Swal.fire("Echec", "Le document n'est pas prêt ", "error");
        }
    })
});
