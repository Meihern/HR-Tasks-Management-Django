
$("#notif-reply a").click(function (e) {
    if ($(this).attr('id') ==='accept-demande-conge'){
    e.preventDefault();
    console.log('test');
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
             swal("Succès","La demande de congé a été acceptée", "success");
        },
        error: function(result) {
            swal("Echec", "Une erreur est survenue ", "error");
        }
    })
}});

$("#notif-reply button").click(function (e) {
    if($(this).attr('id') === 'refuser-demande-conge'){
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
             swal("Succès","La demande de congé a été refusée", "success");
        },
        error: function(result) {
            swal("Echec", "Une erreur est survenue ", "error");
        }
    })
}});