(window.onload = function(){
    var button_name = "edit";
    var target_CSS_selector = 
        "div[typeof='oo:Proof']"
    ;
    var article = document.getElementById('article-panel');
    console.log(article);
    var target_document = article.contentWindow.document;
    console.log(target_document);
    var target_NodeList = target_document.querySelectorAll(target_CSS_selector);
    console.log (target_NodeList);
    
    target_NodeList.forEach(function(value){ value.innerHTML = 
        "<div>"+
            "<form>"+
                "<p><button "+
                " type='button'"+
                " name="+button_name+
                " value="+value.getAttribute("about")+
                ">"+button_name+
                "</button></p>"+
            "</form>"+
        "</div>"
         + value.innerHTML;});
})();