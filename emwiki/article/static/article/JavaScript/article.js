(window.onload = function(){
    //article iframe panel
    var $article = $('#article-panel');
    //current file path in static folder
    var file_path = $article.attr('src');
    //current file name
    var file_name = file_path.slice(file_path.lastIndexOf('/')+1);
    //edit target selector
    var target_CSS_selector = 
        "div[typeof='oo:Proof']"
    ;
    //editBlock
    var editHTML = 
    `<div class='edit'>
        <form class='editForm' method='get' action='/article/' target='_top'>
            <input type='hidden' name='id' value='${file_name}'>
            <input type='hidden' name='proof_name'>
            <button class='editButton' style='inline' type='button'>
            edit
            </button>
            <div class='editblock' style='display:none'>
                <button type='submit' class='submitButton'>submit</button>
                <button type='reset' class='cancelButton'>cancel</button>
                <textarea name='textarea' rows='8' cols='80'></textarea>
            </div>
        </form>
    </div>`

    //add editBlock
    var $target_list = $article.contents().find(target_CSS_selector);
    $target_list.each(function(){
        $(this).prepend(editHTML);
        $(this).find("input[name='proof_name']").attr("value", $(this).attr("about"));
    });

    //editBlock cancelButton clicked
    $article.contents().find(".editForm").on( "click", ".cancelButton", function(){
        console.log("cancelButton pushed");
        var editForm = $(this).parent().parent();
        editForm.find(".editblock").css("display", "none");
        editForm.find(".editbutton").css("display", "inline");
    });
    
    //editBlock editButton clicked
    $article.contents().find(".editForm").on( "click", ".editButton", function(){
        console.log("editButton pushed");
        var editForm = $(this).parent().parent();
        editForm.find(".editblock").css("display", "block");
        editForm.find(".editbutton").css("display", "none");
    });

})();

