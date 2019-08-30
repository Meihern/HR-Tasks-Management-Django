
$("#notif-reply a").click(function (e) {
    if ($(this).attr('id') ==='accept-demande-conge'){
    e.preventDefault();
    let notif_id = $(this).val();
    let csrf = window.CSRF_TOKEN;
    $('#notification-detail-modal').modal('hide');
    Swal.fire({
        title:'Attendez un instant !',
        text: "La demande de congé est en cours de traitement",
    });
    Swal.showLoading({
        allowClickOutside: false,
        allowEscapeKey: false,
        allowEnterKey: false,
    });
    $.ajax({
        url: $(this).data("url"),
        data:{
            'notif_id': notif_id,
            csrfmiddlewaretoken: csrf,
        },
        type: 'POST',
        datatype : 'json',
        success: function(result) {
             Swal.close();
             Swal.fire("Succès","La demande de congé a été acceptée", "success");
        },
        error: function(result) {
            Swal.close();
            Swal.fire("Echec", "Une erreur est survenue ", "error");
        }
    })
}});

$("#notif-reply button").click(function (e) {
    if($(this).attr('id') === 'refuser-demande-conge'){
    e.preventDefault();
    let notif_id = $(this).val();
    let csrf =  CSRF_TOKEN;
    $('#notification-detail-modal').modal('hide');
    Swal.fire({
        title:'Attendez un instant !',
        text: "La demande de congé est en cours de traitement",
    });
    Swal.showLoading({
        allowClickOutside: false,
        allowEscapeKey: false,
        allowEnterKey: false,
    });
    $.ajax({
        url: $(this).data("url"),
        data:{
            'notif_id': notif_id,
            csrfmiddlewaretoken: csrf,
        },
        type: 'POST',
        datatype : 'json',
        success: function(result) {
             Swal.close();
             Swal.fire("Succès","La demande de congé a été refusée", "success");
        },
        error: function(result) {
            Swal.close();
            Swal.fire("Echec", "Une erreur est survenue ", "error");
        }
    })
}});