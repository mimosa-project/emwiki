$(function(){
    var query_text = JSON.parse(document.getElementById('query_text').textContent);
    for(let c of query_text.split('')){
        $('a.subject').highlight(c)
    }
});