$(function(){
    var context = JSON.parse(document.getElementById('context').textContent);
    function jump_to(type=undefined, name=undefined, anchor="", history_method=''){
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
            type: type,
            name: name
        };
        $.getJSON(
            '/contents/index_json',
            body,
            function(index){
                state = {
                    type: index['type'],
                    name: index['name'],
                    anchor: anchor
                }
                if(history_method == 'push'){
                    history.pushState(state, '', `${index['url']}${anchor}`);
                }else if(history_method=='replace'){
                    history.replaceState(state, '', `${index['url']}${anchor}`);
                }
                $('#mml-content')[0].contentWindow.location.replace(`${index['iframe_url']}${anchor}`);
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
    
    jump_to(context['type'], context['name'], location.hash, 'replace')
});