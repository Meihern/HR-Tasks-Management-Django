// Ajax call to retrieve all the received notifications
$("#notifications-toggle").click(function() {
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

//Ajax call to get the details of a single notification

