$(function(){

    function hashHandler(){
        var iframe_url =  '/static/mml-contents/' + location.pathname.split('/').pop() + location.hash;
        $('#mml-content')[0].contentWindow.location.replace(iframe_url);
        select();
    }

    function select(){
        $('#mml-content').contents().find('.selected').removeClass('selected');
        $('#mml-content').contents().find(location.hash).addClass('selected');
    }

    hashHandler();

    window.onhashchange = hashHandler;

    $("#mml-content").on('load', function(){
        let file_path = location.pathname;
        let file_name = file_path.slice(file_path.lastIndexOf('/')+1);
        select();
        $('#mml-content').contents().find("span[data-href]").each( function(){
            $(this).on('click', function(){
                var url;
                url = `/article/${$(this).attr('data-href')}`
                return window.open(url, '_blank').focus();
            })
        });
        $('#mml-content').contents().find(`span[data-link*="${file_name}"]`).each(function(){//`span[data-link]:not([data-link*="${file_name}"])`).each(function(){
            $(this).on('click', function(){
                window.location.href = `/mmlreference/${$(this).attr('data-link')}`
                hashHandler();
            })
        });
        //add iframe.css
        $('#mml-content').contents().find("head").append('<link rel="stylesheet" href="/static/mmlreference/CSS/content.css" type="text/css" />');
    });
});