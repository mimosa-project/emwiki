function search(query, searcher) {
    if ((query != null) && query.length > 0) {
        $("#listdata").empty();
        return searcher.run(query);
    }
}

function input_search_initial_value(searcher) {
    if(Cookies.get('symbol_query')) {
		$('#search-input').val(Cookies.get('symbol_query'));
        return search(Cookies.get('symbol_query'), searcher);
    }
}

$(function(){
	var symbols;
	var searcher;
	$.ajax({
		url: context["names_url"],
		type: "GET",
		dataType: 'json',
		cache: true,
		headers: {
			'Cache-Control': 'max-age=3600, public'
		}
	}).done(function(data){
		symbols = data;
		searcher = new Searcher(data);
		input_search_initial_value(searcher);
	})
	

	$('#search-input').on('keyup', function(){
		search($('#search-input').val(), searcher);
    })
});