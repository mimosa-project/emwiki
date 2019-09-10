(window.onload = function(){
    var target_CSS_selector = 
        "div[typeof='oo:Proof']"
    ;
    var article = document.getElementById('article-panel');
    console.log(article);
    var file_path = article.getAttribute('src');
    var file_name = file_path.slice(file_path.lastIndexOf('/')+1);
    var target_document = article.contentWindow.document;
    console.log(target_document);
    var target_NodeList = target_document.querySelectorAll(target_CSS_selector);
    console.log (target_NodeList);

    target_NodeList.forEach(function(value){ value.innerHTML = 
        `<div class='edit'>
            <form class='editForm' method='get' action='/article/' target='_top'>
                <input type='hidden' name='id' value='${file_name}'>
                <input type='hidden' name='proof_name' value='${value.getAttribute("about")}'>
                <button class='editButton' style='inline' type='button'>
                edit
                </button>
                <div class='editblock' style='display:none'>
                    <button type='submit' class='submitButton'>submit</button>
                    <button type='reset' class='cancelButton'>cancel</button>
                    <textarea name='textarea' rows='8' cols='80'></textarea>
                </div>
            </form>
        </div>
        ${value.innerHTML}`;
    });

    //jQuery
    $("iframe").contents().find(".editForm").on( "click", ".cancelButton", function(){
        console.log("cancelButton pushed");
        var editForm = $(this).parent().parent();
        editForm.find(".editblock").css("display", "none");
        editForm.find(".editbutton").css("display", "inline");
    });

    $("iframe").contents().find(".editForm").on( "click", ".editButton", function(){
        console.log("editButton pushed");
        var editForm = $(this).parent().parent();
        editForm.find(".editblock").css("display", "block");
        editForm.find(".editbutton").css("display", "none");
    });

})();

