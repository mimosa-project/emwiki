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

    // rendering commentPreview from commentTextarea text
    function comment_preview($edit, is_apply_mathjax = true){
        let comment = $edit.find(".commentTextarea").val();
        let commentHTML = commentText2html(comment);
        $edit.find(".commentPreview").html(commentHTML);
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

    //convert commentText to HTML for converion to Tex format
    function commentText2html(commentText){
        let commentText_lines = commentText.split(/\r\n|\r|\n/);
        var html = '';
        if(commentText === ''){
            return html;
        }
        for (let index = 0; index < commentText_lines.length; index++) {
            if (commentText_lines[index]){
                html += `<p>${commentText_lines[index]}</p>`;
            }else{
                html += '<br>'
            }
        }
        //return html;
        return `<p>$${commentText}$</p>`
    }
    function add_emwiki_components(){
        //current file path in static folder
        let file_path =  $article[0].contentDocument.location.pathname;
        //current file name like "abcmiz_0.html"
        let file_name = file_path.slice(file_path.lastIndexOf('/')+1);
        //current article_name like "abcmiz_0"
        let article_name = file_name.split(".")[0];
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
            <button type='button' class='editButton'>+</button>
            <div class='commentPreview mathjax' style='display:block'></div>
            <div class='editcomment' style='display:none'>
                <textarea class='commentTextarea' cols='75' rows='10' wrap='hard'></textarea>
                <div class='toolbar'>
                    <button type='button' class='submitButton'>submit</button>
                    <button type='button' class='cancelButton'>cancel</button>
                    <button type='button' class='previewButton'>preview</button>
                </div>
            </div>
        </span>`;

        //add edit button
        
        $article.contents().find(target_CSS_selector).each(function (target_index, target) {
            //sometimes $(target).text() is like "theorem " so trim()
            target_name = $(target).text().trim();
            let $edit;
            if( target_name in target_object){
                if(target_name === "proof"){
                    $(target).after(editHTML);
                    $edit = $(target).next();
                    $(target).parent().click(function (e) { 
                        $edit.toggle();
                    });
                    $edit.mouseover(function (event) { 
                        event.stopPropagation();
                    });
                    $edit.click(function (event) {
                        event.stopPropagation();
                    })
                    $edit.find(".editButton").click(function (event) {
                        $edit.find(".editcomment").show();
                        $edit.find(".editButton").hide();
                        event.stopPropagation();
                    })
                    $edit.hide();
                    $edit.find(".commentPreview").css("margin-left", "3mm");
                    $edit.find(".editcomment").css("margin-left", "3mm");
                }else{
                    $(target).before(editHTML);
                    $edit = $(target).prev();
                }
                target_object[target_name].push($edit);
                $edit.attr("content", target_name);
                $edit.attr("content_number", target_object[target_name].length);
                $edit.find(".editButton").attr("content", target_name);
            }
        });

        //add comment
        $.getJSON(`/article/data/comment/${article_name}`, function (data, textStatus, jqXHR) {
            for(let content in data["comments"]){
                for(let content_number in data["comments"][content]){
                    $target = $article.contents().find(`
                        .edit[content="${content}"][content_number="${content_number}"]
                    `);
                    $target.find(".commentTextarea").text(data["comments"][content][content_number]);
                    comment_preview($target, false);
                }
            }
        }).done(function(){
            apply_mathjax();
        }).fail(function(){

        });

        
        //edit class editButton clicked
        $article.contents().find('div').on( "click", '.editButton', function(event){
            let $edit = $(this).closest('.edit');
            $edit.find(".editcomment").show();
            $edit.find(".editButton").hide();
            event.stopPropagation();
        });

        //edit class submitButton clicked
        $article.contents().find('div').on( "click", '.submitButton', function(){
            let $edit = $(this).closest('.edit');
            let content = $edit.attr("content");
            let content_number = $edit.attr("content_number");

            //submit proof comment
            $.ajax({
                url: '/article/data/comment/',
                type: 'POST',
                dataType: 'text',
                data: {
                    'content': content,
                    'id': article_name,
                    'content_number': content_number,
                    'comment': $edit.find(".commentTextarea").val()
                },
            }).done(function(data) {
                $edit.find(".editcomment").hide();
                $edit.find(".editButton").show();
                //get proof setch
                $.getJSON(`/article/data/comment/${article_name}`,
                function (data, textStatus, jqXHR) {
                    $edit.find(".commentTextarea").val(data["comments"][content][content_number]);
                }
                ).done(function(){
                    comment_preview($edit);
                }).fail(function(XMLHttpRequest, textStatus, errorThrown){
                    $edit.find(".commentTextarea").val(`failed to fetch error:${textStatus}`);
                    comment_preview($edit);
                    alert(
                        `error : status->${textStatus}
                        failed to get the comment from server`
                    );
                });
            }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
                comment_preview($edit);
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
            $edit.find(".editcomment").hide();
            $edit.find(".editButton").show();
            //get proof comment
            $.getJSON(`/article/data/comment/${article_name}`,
                function (data, textStatus, jqXHR) {
                    $edit.find(".commentTextarea").val(data["comments"][content][content_number]);
                }
            ).done(function(){
                comment_preview($edit);
            }).fail(function(XMLHttpRequest, textStatus, errorThrown){
                $edit.find(".commentTextarea").val(`failed to fetch error:${textStatus}`);
                comment_preview($edit);
                alert(
                    `error : status->${textStatus}
                    failed to get the comment from server`
                );
            });
            
        });
        //edit class previewButton clicked
        $article.contents().find('div').on( "click", '.previewButton', function(){
            comment_preview($(this).closest(".edit"));
        });
        //edit class commentTextarea changed
        $article.contents().find('div').on( "input", '.commentTextarea', function(){
            comment_preview($(this).closest('.edit'));
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