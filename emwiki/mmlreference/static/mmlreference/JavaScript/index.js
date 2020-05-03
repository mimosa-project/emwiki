$(function(){
    console.log(location.pathname)
    
    function jump_to(symbol=undefined, filename=undefined, anchor=""){
        var body = {
            filename: filename,
            symbol: symbol
        };
        $.getJSON(
            '/mmlreference/index_json',
            body,
            function(index){
                history.pushState(
                    {
                        filename: index['filename'],
                        anchor: anchor
                    },
                    '',
                    `/${index['url_subdirectory']}/${index['symbol']}${anchor}`
                );
                $('#mml-content')[0].contentWindow.location.replace(`/${index['static_subdirectory']}/${index['filename']}${anchor}`);
                $('#mml-content').contents().find('.selected').removeClass('selected');
                $('#mml-content').contents().find(location.hash).addClass('selected');
            }
        )
    }

    if (window.history && window.history.pushState) {
        $(window).on('popstate', function(event) {
          var state;
          state = event.originalEvent.state;
          if (state != null) {
            return jump_to(undefined, state.filename, state.anchor);
          } else {
            return jump_to(null);
          }
        });
    }

    jump_to(location.pathname.substr(14), null, '');

    $("#mml-content").on('load', function(){
        let file_path = location.pathname;
        let file_name = file_path.slice(file_path.lastIndexOf('/')+1);
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
                jump_to(null, filename=link[0], `#${anchor=link[1]}`)
            })
        });
        //add iframe.css
        $('#mml-content').contents().find("head").append('<link rel="stylesheet" href="/static/mmlreference/CSS/content.css" type="text/css" />');
    });
});