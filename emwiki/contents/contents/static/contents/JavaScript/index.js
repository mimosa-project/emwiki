var context = JSON.parse(document.getElementById('context').textContent);
var jump_to = function(category=undefined, name=undefined, filename=undefined, anchor="", history_method=''){
    /*
    iframeのページ遷移を行う

    Parameters
    ----------
    category: string
        カテゴリ
    name: string
        名前
    anchor: string
        ページ内アンカー(#付きで入力)
    history_method: string
        ページヒストリへの記録方法(push, replace, other(記録しない))
    */
    var body = {
        category: category,
        name: name,
        filename: filename
    };
    $.getJSON(
        '/contents/normalize_content_url',
        body,
        function(index){
            state = {
                category: index['category'],
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
$(function(){
    if (window.history && window.history.pushState) {
        $(window).on('popstate', function(event) {
            var state;
            state = event.originalEvent.state;
            if (state != null) {
                console.log('popstate:'+state.name+state.anchor)
                return jump_to(state.category, state.name, null, state.anchor, null);
            } else {
                return 
            }
        });
    }
    
    jump_to(context['category'], context['name'], null, location.hash, 'replace')
});