var context = JSON.parse(document.getElementById('context').textContent);
$(function(){
    function select(anchor){
        //アンカーされているコンテンツをマーク(CSSでborderを指定して囲むため)
        $("#symbol").find('.selected').removeClass('selected');
        $("#symbol").find(anchor).addClass('selected');
    }
    select(location.anchor);
    $("#symbol").find("span[data-href]").each( function(){
        $(this).on('click', function(){
            var url = encodeURI(context['article_base_uri'] + $(this).attr('data-href'));
            return window.open(url, '_blank').focus();
        })
    });

    $("#symbol").find(`span[data-link]`).each(function(){
        $(this).on('click', function(){
            let url = undefined;
            var link = $(this).attr('data-link').split("#");
            $.get({
                url: context["adjust_name_url"],
                data: {name: link[0]},
            }).done(function (data) {
                location.href = encodeURI(`${data}#${link[1]}`);
            select(link[1]);
            }).fail(function(XMLHttpRequest, textStatus, errorThrown){
                console.log('Failed to get symbol name\n' + textStatus);
            });
        })
    });
});