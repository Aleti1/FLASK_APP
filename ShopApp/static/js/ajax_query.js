$(document).ready(function(){
    
    $.ajax({
        type: "GET",
        url: "http://myserver:5000/query",
        //dataType: 'json',
        success: function(data) {
            console.log("This is the returned data: " + JSON.stringify(data));
        },
        error: function(error){
            console.log("Here is the error res: " + JSON.stringify(error));
        }
    });
});