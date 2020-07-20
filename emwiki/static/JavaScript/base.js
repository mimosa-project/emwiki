$(function(){
    $.ajax({
        url: '/search/get_keywords',
        type: 'GET',
        dataType: 'json',
        timespan: 1000
    }).done( response => {
        for(var keyword of response.keywords){
            $('#search_keywords').append('<option value="' + keyword + '">')
        }
    }) 
})
