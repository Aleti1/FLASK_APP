function form_submit( action ){
    var form = $(action).closest('form'),
        link = $(form).data('action'),
        method = $(form).data('method'),
        func = $(form).data('function'),
        post = new FormData(form[0]),
        message = $(form).find('.message'),
        input = '.input',
        input_message = '.input-message',
        base_url = window.location.origin = window.location.protocol+'//'+window.location.host;
        link = base_url+'/'+link;

    $(message).html('');
    $(form).find(input_message).html('');

    $.ajax({
        type: method,
        url: link,
        data: post,
        success: function(response){
            response = JSON.parse(response);
            if(response.error == 0){
                if(func in window){
                    window[func](action, response);
                }
                if('message' in response){
                    $(message).html(response.message); 
                }
            } else if(response.error == 1){
                window.location.href = base_url;
            } else if(response.error == 2){
                $.each(response.errors, function(k){
                    $(form).find('input[name="'+k+'"]').closest(input).find(input_message).html(response.errors[k]);
                });  
            } else if(response.error == 3){
                if(func in window){
                    window[func](action, response);
                }
                $(message).html(respone.message);
            }
        },
        cache: false,
        contentType: false,
        processData: false
    });

}