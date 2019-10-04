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
    function sketch_preview($edit, is_apply_mathjax = true){
        let sketch = $edit.find(".sketchTextarea").val();
        let sketchHTML = sketchText2html(sketch);
        $edit.find(".sketchPreview").html(sketchHTML);
        if(is_apply_mathjax){
            apply_mathjax();
        }
    }

    //Apply MathJax class="mathjax"
    //This function is not guaranteed to work when MathJax in iframe is updated
    function apply_mathjax(){
        let iframe_MathJax = $article[0].contentWindow.MathJax;
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
        let target_CSS_selector = 'span.kw';
        //target DOMs list
        let target_object = {
            'definition': [],
            'theorem': [],
            'registration': [],
            'scheme': [],
            'notation': [],
            'proof': []
        };
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

        //add edit button
        
        $article.contents().find(target_CSS_selector).each(function (target_index, target) {
            //sometimes $(target).text() is like "theorem " so trim()
            target_name = $(target).text().trim();
            if( target_name in target_object){
                $(target).before(editHTML);
                let $edit = $(target).prev();
                target_object[target_name].push($edit);
                $edit.attr("content", target_name);
                $edit.attr("content_number", target_object[target_name].length);
                $edit.find(".editButton").attr("content", target_name);
            }
        });

        //add sketch
        $.getJSON(`/article/data/${file_name.split(".")[0]}`, function (data, textStatus, jqXHR) {
            for(let content in data["sketches"]){
                for(let content_number in data["sketches"][content]){
                    $target = $article.contents().find(`
                        .edit[content="${content}"][content_number="${content_number}"]
                    `);
                    $target.find(".sketchTextarea").text(data["sketches"][content][content_number]);
                    sketch_preview($target, false);
                }
            }
        }).done(function(){
            apply_mathjax();
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
            let content = $edit.attr("content");
            let content_number = $edit.attr("content_number");

            //submit proof sketch
            $.ajax({
                url: '/article/sketch/',
                type: 'POST',
                dataType: 'text',
                data: {
                    'content': content,
                    'id': file_name,
                    'content_number': content_number,
                    'sketch': $edit.find(".sketchTextarea").val()
                },
            }).done(function(data) {
                $edit.find(".editSketch").css("display", "none");
                $edit.find(".editButton").css("display", "inline");
                //get proof setch
                $.getJSON(`/article/data/${file_name.split(".")[0]}`,
                function (data, textStatus, jqXHR) {
                    $edit.find(".sketchTextarea").val(data["sketches"][content][content_number]);
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
            let content = $edit.attr("content");
            let content_number = $edit.attr("content_number");
            $edit.find(".editSketch").css("display", "none");
            $edit.find(".editButton").css("display", "inline");
            //get proof sketch
            $.getJSON(`/article/data/${file_name.split(".")[0]}`,
                function (data, textStatus, jqXHR) {
                    $edit.find(".sketchTextarea").val(data["sketches"][content][content_number]);
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