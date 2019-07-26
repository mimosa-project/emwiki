(window.onload = function(){
var head_string = "edit"
var page = document.getElementById('page-panel');
console.log(page);
var page_theorem = page.contentWindow.document;
console.log(page_theorem);
page_theorem = page_theorem.querySelectorAll('div[typeof="oo:Theorem"]');
console.log (page_theorem);

page_theorem.forEach(function(value){ value.innerHTML = "<div><a>"+head_string+"</a></div>" + value.innerHTML;});
})();