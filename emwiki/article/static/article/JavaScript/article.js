(window.onload = function(){
    var button_name = "edit";
    var target_CSS_selector = 
        "div[typeof='oo:Proof']"
    ;
    var article = document.getElementById('article-panel');
    console.log(article);
    var file_path = article.getAttribute('src');
    var file_name = file_path.slice(file_path.lastIndexOf('/')+1);
    var target_document = article.contentWindow.document;
    console.log(target_document);
    //apply iframe.js to iframe
    var el = target_document.createElement("script");
    el.src = "/static/article/JavaScript/iframe.js";
    target_document.body.appendChild(el);
    var target_NodeList = target_document.querySelectorAll(target_CSS_selector);
    console.log (target_NodeList);
    
    target_NodeList.forEach(function(value){ value.innerHTML = 
        "<div>"+
            "<form method='get' action='/article/'"+
                " target='_top'>"+
                "<input type='hidden' name='id' value='"+file_name+"'>"+
                "<input type='hidden' name='proof_name' value='"+value.getAttribute("about")+"'>"+
                "<button style='inline' "+
                " type='button'"+
                " name="+button_name+
                " value="+value.getAttribute("about")+
                " onclick=editButtonClicked(this)"+
                ">"+button_name+
                "</button>"+
                "<div name='editBlock' style='display:none'>"+
                    "<button type='submit' name='submit'>submit</button>"+
                    "<button type='reset' name='cancel' onclick='cancelButtonClicked(this)'>cancel</button>"+
                    "<textarea name='textarea' rows='8' cols='80'></textarea>"+
                "</div>"+
            "</form>"+
        "</div>"+
        value.innerHTML;});
})();

