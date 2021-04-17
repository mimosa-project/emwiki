class Initializer {
    static initialize() {
        this.set_csrf_token_on_post();

    }

    static set_csrf_token_on_post() {
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
    }
}


class Article {

}

class Comment {
    preview() {

    }

    reder() {

    }
    // rendering commentPreview from commentTextarea text
    function comment_preview($target_list){
        //Apply MathJax class="mathjax"
        //This function is not guaranteed to work when MathJax in iframe is updated
        function apply_mathjax(){
            let iframe_MathJax = $article[0].contentWindow.MathJax;
            if(iframe_MathJax){
                iframe_MathJax.typeset();
            }
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
            return `<p>${commentText}</p>`
        }

        for($target of $target_list){
            let comment = $target.find(".commentTextarea").val();
            let commentHTML = commentText2html(comment);
            $target.find(".commentPreview").html(commentHTML);
        }
        apply_mathjax();
    }

}

$(function(){
    let $article = $('#article');
    var context = JSON.parse(document.getElementById('context').textContent);

    let initializer = new Initializer();
    initializer.initialize();

    $('[data-toggle="popover"]').popover()
    
    add_emwiki_components($article);

    //edit class editButton clicked
    $article.contents().find('body').on( "click", '.editButton', function(event){
        let $edit = $(this).closest('.edit');
        $edit.find(".editcomment").show();
        $edit.find(".editButton").hide();
        event.stopPropagation();
    });

    //edit class submitButton clicked
    $article.contents().find('body').on( "click", '.submitButton', function(){
        let $edit = $(this).closest('.edit');
        let block = $edit.attr("block");
        let block_order = $edit.attr("block_order");
        //submit proof comment
        $.ajax({
            url: context['comment_url'],
            type: 'POST',
            dataType: 'text',
            data: {
                'block': block,
                'article_name': context['name'],
                'block_order': block_order,
                'comment': $edit.find(".commentTextarea").val()
            },
        }).done(function(data) {
            $edit.find(".editcomment").hide();
            $edit.find(".editButton").show();
            fetch_comment([$edit,])
        }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
            comment_preview([$edit,]);
            alert(
                `error : status->${textStatus}
                !!!Not yet saved!!!`
            );
        });
    });

    //edit class cancelButton clicked
    $article.contents().find('body').on( "click", '.cancelButton', function(){
        let $target = $(this).closest('.edit');
        $target.find(".editcomment").hide();
        $target.find(".editButton").show();

        fetch_comment([$target,])
    });
    //edit class previewButton clicked
    $article.contents().find('body').on( "click", '.previewButton', function(){
        comment_preview([$(this).closest(".edit"),]);
    });
    //edit class commentTextarea changed
    $article.contents().find('body').on( "input", '.commentTextarea', function(){
        comment_preview([$(this).closest('.edit'),]);
    });

    // rendering commentPreview from commentTextarea text
    function comment_preview($target_list){
        //Apply MathJax class="mathjax"
        //This function is not guaranteed to work when MathJax in iframe is updated
        function apply_mathjax(){
            let iframe_MathJax = $article[0].contentWindow.MathJax;
            if(iframe_MathJax){
                iframe_MathJax.typeset();
            }
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
            return `<p>${commentText}</p>`
        }

        for($target of $target_list){
            let comment = $target.find(".commentTextarea").val();
            let commentHTML = commentText2html(comment);
            $target.find(".commentPreview").html(commentHTML);
        }
        apply_mathjax();
    }

    function fetch_comment($target_list){
        console.log("fetch comment!")
        let body = {querys: []}
        for(let $target of $target_list){
            let block = $target.attr("block");
            let block_order = $target.attr("block_order");
            body.querys.push({
                article_name: context['name'],
                block: block,
                block_order: block_order
            })
        }
        $.ajax({
            type: 'GET',
            url: `${context['comment_url']}`,
            dataType: 'json',
            contentType: 'application/json',
            data: {'article_name': context['name']}
        }).done(function (data, textStatus, jqXHR) {
            comments = data['comments']
            for(comment of comments){
                $target = $article.contents().find(`
                    .edit[block="${comment['block']}"][block_order="${comment['block_order']}"]
                `);
                $target.find(".commentTextarea").val(comment['text']);
            }
        }).fail(function(XMLHttpRequest, textStatus, errorThrown){
            console.log(XMLHttpRequest.textStatus)
            alert('Failed to get some comment\n' + textStatus);
        }).always(function(){
            comment_preview($target_list)
        });
    }
    
    function add_emwiki_components(){
        //current file path in static folder
        let file_path =  location.pathname;
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

        let editHTML = 
        `<span class='edit'>
            <div class='commentPreviewWrapper'>
            <div class='commentPreview mathjax' style='display:block'></div>
            </div>
            <button type='button' class='editButton'>+</button>
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
        let $edit_list = []
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
                $edit.attr("block", target_name);
                $edit.attr("block_order", target_object[target_name].length);
                $edit.find(".editButton").attr("block", target_name);
                $edit_list.push($edit)
            }
        });

        fetch_comment($edit_list)
    }
});