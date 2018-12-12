function get_db_backup() {
    $.post( "database/create_backups", {}, function() {
        console.log( "successfully requested db backups" );
    })
        .done(function(data) {
            if (data.success == false) {
                window.alert(data.error);
            } else {
                window.open(data.url, '_blank');
            }
        })
        .fail(function(err) {
            console.log(err);
        });
}