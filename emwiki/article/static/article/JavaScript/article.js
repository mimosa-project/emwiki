$(function(){
    let $article = $('#article');

    $("#article").on( 'load',function(){
        //add base directory
        $article.contents().find("head").prepend("<base href='/static/mizar_html/'/>");
        //add iframe.css
        $article.contents().find("head").append('<link rel="stylesheet" href="/static/article/CSS/iframe.css" type="text/css" />');
        let file_path = $article[0].contentDocument.location.pathname;
        let file_name = file_path.slice(file_path.lastIndexOf('/')+1);
        add_emwiki_components($article);
        $('#file_name').text(file_name);
        $article[0].contentWindow.onbeforeunload = function () {
            $("#file_name").text("Now Loading...");
        };
    });

    // rendering sketchPreview from sketchTextarea text
    function sketch_preview($edit){
        let iframe_MathJax = $article[0].contentWindow.MathJax;
        let sketch = $edit.find(".sketchTextarea").val();
        let sketchHTML = sketchText2html(sketch);
        $edit.find(".sketchPreview").html(sketchHTML);
        iframe_MathJax.Hub.Queue(["Typeset",iframe_MathJax.Hub]);
    }

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
        let target_CSS_selector;
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
        $.getJSON(`/article/data/${file_name.split(".")[0]}`,
            function (data, textStatus, jqXHR) {
                for(ref_name in data.refs){
                    target_CSS_selector = `div[about="#${ref_name}"]`;
                    let $target = $article.contents().find(target_CSS_selector);
                    $target.prepend(editHTML);
                    $target.find(".edit").attr("content", "refs");
                    $target.find(".edit").attr("content-name", ref_name);
                    $target.find(".sketchTextarea").text(data.refs[ref_name]);
                    $target.find(".sketchPreview").html(sketchText2html(data.refs[ref_name]));
                }
                for(proof_name in data.proofs){
                    target_CSS_selector = `div[about="#PF${proof_name}"]`;
                    let $target = $article.contents().find(target_CSS_selector);
                    $target.prepend(editHTML);
                    $target.find(".edit").attr("content", "proofs");
                    $target.find(".edit").attr("content-name", proof_name);
                    $target.find(".sketchTextarea").text(data.proofs[proof_name]);
                    $target.find(".sketchPreview").html(sketchText2html(data.proofs[proof_name]));
                }
            }
        ).done(function(){
            iframe_MathJax.Hub.Queue(["Typeset",iframe_MathJax.Hub]);
        }).fail(function(){

        });

        
        //edit class editButton clicked
        $article.contents().find('div').on( "click", '.editButton', function(){
            let $edit = $(this).closest('.edit');
            $edit.find(".editSketch").css("display", "block");
            $edit.find(".editButton").css("display", "none");
        });

        //edit class submitButton clicked
        $article.contents().find('div').on( "click", '.submitButton', function(){
            let $edit = $(this).closest('.edit');
            let name = $edit.attr("content-name");
            let content = $edit.attr("content");

            //submit proof sketch
            $.ajax({
                url: '/article/sketch/',
                type: 'POST',
                dataType: 'text',
                data: {
                    'content': content,
                    'id': file_name,
                    'name': name,
                    'sketch': $edit.find(".sketchTextarea").val()
                },
            }).done(function(data) {
                $edit.find(".editSketch").css("display", "none");
                $edit.find(".editButton").css("display", "inline");
                //get proof setch
                $.getJSON(`/article/data/${file_name.split(".")[0]}`,
                function (data, textStatus, jqXHR) {
                    $edit.find(".sketchTextarea").val(data[content][name]);
                }
                ).done(function(){
                    sketch_preview($edit);
                }).fail(function(XMLHttpRequest, textStatus, errorThrown){
                    $edit.find(".sketchTextarea").val(`failed to fetch error:${textStatus}`);
                    sketch_preview($edit);
                    alert(
                        `error : status->${textStatus}
                        failed to get the sketch from server`
                    );
                });
            }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
                sketch_preview($edit);
                alert(
                    `error : status->${textStatus}
                    !!!Not yet saved!!!`
                );
            });

        });

        //edit class cancelButton clicked
        $article.contents().find('div').on( "click", '.cancelButton', function(){
            let $edit = $(this).closest('.edit');
            let name = $edit.attr("content-name");
            let content = $edit.attr("content");
            $edit.find(".editSketch").css("display", "none");
            $edit.find(".editButton").css("display", "inline");
            //get proof sketch
            $.getJSON(`/article/data/${file_name.split(".")[0]}`,
                function (data, textStatus, jqXHR) {
                    $edit.find(".sketchTextarea").val(data[content][name]);
                }
            ).done(function(){
                sketch_preview($edit);
            }).fail(function(XMLHttpRequest, textStatus, errorThrown){
                $edit.find(".sketchTextarea").val(`failed to fetch error:${textStatus}`);
                sketch_preview($edit);
                alert(
                    `error : status->${textStatus}
                    failed to get the sketch from server`
                );
            });
            
        });
        //edit class previewButton clicked
        $article.contents().find('div').on( "click", '.previewButton', function(){
            sketch_preview($(this).closest(".edit"));
        });
        //edit class sketchTextarea changed
        $article.contents().find('div').on( "input", '.sketchTextarea', function(){
            sketch_preview($(this).closest('.edit'));
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