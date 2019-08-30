// Ajax call to retrieve all the unseen received notifications

$("#notifications-toggle").click(function(e) {

        $.ajax({
            url: $(this).data("url"),
            type: 'GET',
            dataType: 'json',
            success: function(data) { // success is the callback when the server responds
                /* if is json what you decided to return then process the json dict
                   if is normal html render it wherver you want
                */
                $('#notifications-get').empty().append(data.notifications.map((notifications) => {
                    var time_sent = new Date(notifications.time_sent);
                    time_sent = time_sent.toLocaleDateString('fr-FR',
                        {
                            day:'numeric',
                            month: 'short',
                            year: 'numeric',
                            hour: 'numeric',
                            minute: 'numeric',
                        });
                    return $('<a class="dropdown-item d-flex align-items-center" data-url="notifications/get_notification_detail" href="#" data-value="'+notifications.id+'" data-toggle="modal" data-target="#notification-detail-modal" >' +
                        '<div class="mr-3">' +
                        '<div class="icon-circle bg-primary">' +
                        '<i class="fas fa-file-alt text-white"></i>' +
                        '</div>' +
                        '</div>' +
                        '<div>' +
                        '<div class="small text-gray-500"> le ' + time_sent + '</div>' +
                        '<span class="font-weight-bold">' + notifications.subject +'</span>'+
                        '</div>'+
                        '</a>');
                }));
            }
        });
});

//Ajax call to get all notifications received

$('#notification-all-modal').on("show.bs.modal", function(e){
    $.ajax({
        url: $("#get-all-notifications").data("url"),
        type: 'GET',
        dataType: 'json',
        success: function(data) {
                console.log("Success");
                $('#modal-body-notification-all').empty().append(data.notifications.map((notifications) => {
                    let time_sent = new Date(notifications.time_sent);
                    time_sent = time_sent.toLocaleDateString('fr-FR',
                        {
                            day:'numeric',
                            month: 'short',
                            year: 'numeric',
                            hour: 'numeric',
                            minute: 'numeric',
                        });
                    let seen;
                    if (notifications.seen === true) seen = 'Vue';
                    else seen = 'Non Vue';
                    return $(
                        '<a class="dropdown-item d-flex align-items-center" data-url="notifications/get_notification_detail" href="#" data-value="'+notifications.id+'" data-toggle="modal" data-target="#notification-detail-modal" >' +
                        '<div class="mr-3">' +
                        '<div class="icon-circle bg-primary">' +
                        '<i class="fas fa-file-alt text-white"></i>' +
                        '</div>' +
                        '</div>' +
                        '<div>' +
                        '<span class="font-weight-bold">' + notifications.subject +'</span><br>'+
                        '<div class="small text-gray-500">le ' + time_sent + '</div>' +
                        '<span class="small text-gray-500"> Envoyé par ' + notifications.sender__full_name + '</span><br>'+
                        '<span class="small text-info">'+seen+'</span>'+
                        '</div>'+
                        '</a>'
                    );
                }));
        }
    });
});


