$(function(){

    $(".article").on( 'load',function(){
        //add base directory
        $('.article').contents().find("head").prepend("<base href='/static/mizar_html/'/>");
        var history_text = $('.article')[0].contentDocument.location.pathname;
        history_text = history_text.slice(history_text.lastIndexOf('/')+1);
        $('.history').text(history_text);
        add_edit_button($(".article"));
    });

    function add_edit_button($iframe){
        //current file path in static folder
        var file_path = $iframe.attr('src');
        //current file name
        var file_name = file_path.slice(file_path.lastIndexOf('/')+1);
        //edit target selector
        var target_CSS_selector = 
            "div[typeof='oo:Proof']"
        ;

        var editHTML = 
        `<div class='edit'>
            <button type='button' class='editButton'>
            edit
            </button>
            <div class='editSketch' style='display:none'>
                <button type='button' class='submitButton'>submit</button>
                <button type='button' class='cancelButton'>cancel</button>
                <textarea class='sketchTextarea' rows='8' cols='80' style='display:block'></textarea>
            </div>
        </div>`

        //add edit class
        var $target_list = $iframe.contents().find(target_CSS_selector);
        $target_list.each(function(){
            $(this).prepend(editHTML);
            var proof_name = $(this).attr("about").slice($(this).attr("about").lastIndexOf("#PF")+3);
            $(this).find(".edit").attr("proof_name", proof_name);
        });
        //edit class editButton clicked
        $iframe.contents().find('.editButton').on( "click", function(){
            var $edit = $(this).parents('.edit');
            $edit.find(".editSketch").css("display", "block");
            $edit.find(".editButton").css("display", "none");
        });

        //edit class submitButton clicked
        $iframe.contents().find('.submitButton').on( "click", function(){
            var $edit = $(this).parents('.edit');
            var proof_name = $edit.attr("proof_name");
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
                alert("error");
            });

        });
        //edit class cancelButton clicked
        $iframe.contents().find('.cancelButton').on( "click", function(){
            var $edit = $(this).parents('.edit');
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