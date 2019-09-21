$(function(){
    let $article = $('#article');

    $("#article").on( 'load',function(){
        //add base directory
        $article.contents().find("head").prepend("<base href='/static/mizar_html/'/>");
        let file_path = $article[0].contentDocument.location.pathname;
        let file_name = file_path.slice(file_path.lastIndexOf('/')+1);
        add_emwiki_components($article);
        $('#file_name').text(file_name);
        $article[0].contentWindow.onbeforeunload = function () {
            $("#file_name").text("Now Loading...");
        };
    });

    //convert sketchText to HTML for converion to Tex format
    function sketchText2html(sketchText){
        let sketchText_lines = sketchText.split(/\r\n|\r|\n/);
        var html = '';
        if(sketchText === ''){
            return html;
        }
        for (let index = 0; index < sketchText_lines.length; index++) {
            if (sketchText_lines[index]){
                html += `<p>${sketchText_lines[index]}</p>`;
            }else{
                html += '<br>'
            }
        }
        return html;
    }
    function add_emwiki_components(){
        //current file path in static folder
        let file_path =  $article[0].contentDocument.location.pathname;
        //current file name
        let file_name = file_path.slice(file_path.lastIndexOf('/')+1);
        //edit target selector
        let target_CSS_selector = 
            "div[typeof='oo:Proof']"
        ;
        let iframe_MathJax = $article[0].contentWindow.MathJax;

        let editHTML = 
        `<span class='edit'>
            <div class='sketchPreview mathjax'></div>
            <div class='editSketch' style='display:none'>
                <textarea class='sketchTextarea'></textarea>
                <button type='button' class='submitButton'>submit</button>
                <button type='button' class='cancelButton'>cancel</button>
                <button type='button' class='previewButton'>preview</button>
            </div>
            <button type='button' class='editButton'>+</button>
        </span>`;

        //add edit class
        let $target_list = $article.contents().find(target_CSS_selector);
        $target_list.each(function(index){
            let $target = $(this);
            $target.prepend(editHTML);
            let proof_name = $target.attr("about").slice($target.attr("about").lastIndexOf("#PF")+3);
            $target.find(".edit").attr("proof_name", proof_name);
        });
        //edit class editButton clicked
        $article.contents().find('.editButton').on( "click", function(){
            let $edit = $(this).closest('.edit');
            $edit.find(".editSketch").css("display", "block");
            $edit.find(".editButton").css("display", "none");
        });

        //edit class submitButton clicked
        $article.contents().find('.submitButton').on( "click", function(){
            let $edit = $(this).closest('.edit');
            let proof_name = $edit.attr("proof_name");
            $edit.find(".editSketch").css("display", "none");
            $edit.find(".editButton").css("display", "inline");
            $.ajax({
                url: '/article/data/',
                type: 'POST',
                dataType: 'text',
                data: {
                    'content': 'proof_sketch',
                    'id': file_name,
                    'proof_name': proof_name,
                    'proof_sketch': $edit.find(".sketchTextarea").val()
                },
            }).done(function(data) {
                alert("sent");
            }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
                alert(
                    `error : status->${textStatus}
                    !!!Not yet saved!!!`
                );
            });

        });
        //edit class cancelButton clicked
        $article.contents().find('.cancelButton').on( "click", function(){
            var $edit = $(this).closest('.edit');
            $edit.find(".editSketch").css("display", "none");
            $edit.find(".editButton").css("display", "inline");
        });
    }


    
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    //get csrf_token from cookie
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});