$(function(){
    function select(anchor){
        //アンカーされているコンテンツをマーク(CSSでborderを指定して囲むため)
        $('#mml-content').contents().find('.selected').removeClass('selected');
        $('#mml-content').contents().find(anchor).addClass('selected');
    }
    select(location.anchor);

    $("#mml-content").on('load', function(){
        select(location.hash);

        $('#mml-content').contents().find("span[data-href]").each( function(){
            $(this).on('click', function(){
                var url;
                url = `/contents/Article/${$(this).attr('data-href')}`
                return window.open(url, '_blank').focus();
            })
        });

        $('#mml-content').contents().find(`span[data-link]`).each(function(){
            $(this).on('click', function(){
                var link = $(this).attr('data-link').split("#");
                jump_to('Symbol', null, filename=link[0], `#${anchor=link[1]}`, 'push')
                select(link[1]);
            })
        });
    });
});