
$("#accept-demande-conge").click(function (e) {
    e.preventDefault();
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
             swal("Succès","La demande de congé a été acceptée");
        },
        error: function(result) {
            swal("Echec", "Une erreur est survenue ", "error");
        }
    })
});

$("#refuser-demande-conge").click(function (e) {
    e.preventDefault();
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
             swal("Succès","La demande de congé a été refusée");
        },
        error: function(result) {
            swal("Echec", "Une erreur est survenue ", "error");
        }
    })
});