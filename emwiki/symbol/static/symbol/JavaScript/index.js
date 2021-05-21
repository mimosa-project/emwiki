var context = JSON.parse(document.getElementById('context').textContent);
$(function(){
    function select(anchor){
        //アンカーされているコンテンツをマーク(CSSでborderを指定して囲むため)
        $("#symbol").find('.selected').removeClass('selected');
        $("#symbol").find(anchor).addClass('selected');
    }
    select(location.anchor);
    $("#main").on('click', 'span[data-href]', function(){
        var url = encodeURI(context['article_base_uri'] + $(this).attr('data-href'));
        return window.open(url, '_blank').focus();
    })

    $("#main").on('click', '[data-link]' , function(){
        let url = undefined;
        var link = $(this).attr('data-link').split("#");
        link[0] = decodeURIComponent(link[0]);
        Cookies.set('symbol_query', $("#search-input").val(), { expires: 1 })
        $.get({
            url: context["adjust_name_url"],
            data: {name: link[0]},
        }).done(function (data) {
            location.href = `${encodeURIComponent(data)}#${encodeURIComponent(link[1])}`;
        select(link[1]);
        }).fail(function(XMLHttpRequest, textStatus, errorThrown){
            console.log('Failed to get symbol name\n' + textStatus);
        });
    })
});