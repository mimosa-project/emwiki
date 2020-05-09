$(function(){
    console.log(location.pathname)
    
    function jump_to(symbol=undefined, filename=undefined, anchor="", history_method=''){
        /*
        iframeのページ遷移を行う

        Parameters
        ----------
        symbol: string
            シンボル名
        filename: string
            ファイル名
        anchor: string
            ページ内アンカー(#付きで入力)
        history_method: string
            ページヒストリへの記録方法(push, replace, other(記録しない))
        */
        console.log('jump_to')
        var body = {
            filename: filename,
            symbol: symbol
        };
        $.getJSON(
            '/symbol/index_json',
            body,
            function(index){
                state = {
                    filename: index['filename'],
                    anchor: anchor
                }
                if(history_method == 'push'){
                    history.pushState(state, '', `/${index['url_subdirectory']}/${index['symbol']}${anchor}`);
                }else if(history_method=='replace'){
                    history.replaceState(state, '', `/${index['url_subdirectory']}/${index['symbol']}${anchor}`);
                }
                $('#mml-content')[0].contentWindow.location.replace(`/${index['static_subdirectory']}/${index['filename']}${anchor}`);
                select(anchor)
            }
        )
    }

    if (window.history && window.history.pushState) {
        $(window).on('popstate', function(event) {
            var state;
            state = event.originalEvent.state;
            if (state != null) {
                console.log('popstate:'+state.filename+state.anchor)
                return jump_to(undefined, state.filename, state.anchor, null);
            } else {
                return 
            }
        });
    }

    function select(anchor){
        //アンカーされているコンテンツをマーク(CSSでborderを指定して囲むため)
        $('#mml-content').contents().find('.selected').removeClass('selected');
        $('#mml-content').contents().find(anchor).addClass('selected');
    }

    jump_to(location.pathname.substr(14), null, '', 'replace');

    $("#mml-content").on('load', function(){
        console.log('iframe loaded')
        select(location.hash);

        $('#mml-content').contents().find("span[data-href]").each( function(){
            $(this).on('click', function(){
                var url;
                url = `/article/${$(this).attr('data-href')}`
                return window.open(url, '_blank').focus();
            })
        });

        $('#mml-content').contents().find(`span[data-link]`).each(function(){
            $(this).on('click', function(){
                var link = $(this).attr('data-link').split("#");
                jump_to(null, filename=link[0], `#${anchor=link[1]}`, 'push')
            })
        });
        //add iframe.css
        $('#mml-content').contents().find("head").append('<link rel="stylesheet" href="/static/symbol/CSS/content.css" type="text/css" />');
    });
});